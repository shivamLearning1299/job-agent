# ── backend/agent.py ──────────────────────────────────────────

from dotenv import load_dotenv
load_dotenv()

import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langfuse_config import get_langfuse_handler
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# ── STEP 1: Load ChromaDB (our resume brain) ──────────────────
def load_vectorstore():
    """
    We don't re-ingest the resume every time.
    We just reconnect to the existing ChromaDB on disk.
    Like opening a database connection.
    """
    print("📂 Loading ChromaDB...")

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    )

    vectorstore = Chroma(
        persist_directory=os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"),
        embedding_function=embeddings,
        collection_name="resume"
    )

    print("✅ ChromaDB loaded!")
    return vectorstore


# ── STEP 2: Build the RAG chain ───────────────────────────────
def build_rag_chain(vectorstore):
    """
    RAG = Retrieval Augmented Generation

    Step 1 (Retrieval): Search ChromaDB for resume chunks
                        that are relevant to the JD
    Step 2 (Augmented): Add those chunks to the prompt
                        as context for the LLM
    Step 3 (Generation): LLM reads JD + resume chunks
                         and generates tailored output
    """
    print("🔗 Building RAG chain...")

    # The LLM that will do the thinking and writing
    # temperature=0.3 means slightly creative but mostly focused
    # temperature=0   = robotic, always same answer
    # temperature=1   = very creative, sometimes random
    llm = ChatOllama(
        model="qwen2.5:14b",
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0.3
    )

    # Retriever: searches ChromaDB and returns top 4 matching chunks
    # k=4 means "give me the 4 most relevant resume chunks"
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    # The prompt template — this is the instruction we give the LLM
    # {context} = the 4 resume chunks retrieved from ChromaDB
    # {question} = the job description the user pastes
    prompt_template = """
You are an expert career coach and resume writer.

You have been given relevant sections from a candidate's resume below.
Use ONLY this resume content to answer — do not make up experience.

RESUME SECTIONS:
{context}

JOB DESCRIPTION:
{question}

Your task:
1. TAILORED BULLETS: Rewrite 4-5 resume bullets that best match 
   this job description. Use the JD's exact keywords and language.
   Keep bullets strong and action-oriented (started with verbs).

2. SKILL GAPS: List skills mentioned in the JD that are NOT found
   in the resume. Be specific. Format as a simple list.

Format your response exactly like this:

TAILORED BULLETS:
- [bullet 1]
- [bullet 2]
- [bullet 3]
- [bullet 4]
- [bullet 5]

SKILL GAPS:
- [gap 1]
- [gap 2]
- [gap 3]
"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    # RetrievalQA chain ties everything together:
    # user question → retriever finds chunks → prompt + chunks → LLM → answer
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",      # "stuff" = put all chunks into one prompt
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True   # also return which chunks were used
    )

    print("✅ RAG chain ready!")
    return chain


# ── STEP 3: Run the agent ─────────────────────────────────────
def analyze_jd(jd_text: str):
    print("\n🤖 Analyzing job description...")

    vectorstore = load_vectorstore()
    chain = build_rag_chain(vectorstore)

    # Get LangFuse handler
    langfuse_handler = get_langfuse_handler()

    # Pass handler as callback — LangFuse now watches every step
    config = {}
    if langfuse_handler:
        config = {"callbacks": [langfuse_handler]}

    # invoke now passes the callback config
    result = chain.invoke(
        {"query": jd_text},
        config=config        # ← this is the only change here
    )

    answer = result["result"]
    sources = result["source_documents"]

    print("\n📋 RESULT:")
    print(answer)

    print(f"\n📎 Used {len(sources)} resume chunks as context:")
    for i, doc in enumerate(sources):
        print(f"  Chunk {i+1}: {doc.page_content[:80]}...")

    # Flush ensures all traces are sent to LangFuse
    # before the script exits
    print("\n📊 Trace sent to LangFuse dashboard!")

    return answer

# ── TEST: Run directly to test ────────────────────────────────
if __name__ == "__main__":
    # Paste any job description here to test
    test_jd = """
    We are looking for a Senior Backend Engineer with experience in:
    - Python and FastAPI
    - Building and deploying AI/ML models
    - RAG pipelines and vector databases
    - REST API design
    - Docker and cloud deployment (AWS/GCP)
    - SQL and NoSQL databases
    """

    analyze_jd(test_jd)
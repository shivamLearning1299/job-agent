# ── backend/ingest.py ──────────────────────────────────────────

# python-dotenv reads our .env file and loads the variables
from dotenv import load_dotenv
load_dotenv()

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# ── STEP 1: Load your resume PDF ───────────────────────────────
# Change this path to wherever your resume PDF is on your Mac
RESUME_PATH = "./resume.pdf"

def load_resume(path: str):
    """
    PyPDFLoader reads the PDF page by page.
    Each page becomes a 'Document' object with:
      - page_content : the actual text
      - metadata     : { source: path, page: 0 }
    """
    print(f"📄 Loading resume from: {path}")
    loader = PyPDFLoader(path)
    pages = loader.load()
    print(f"✅ Loaded {len(pages)} page(s)")
    return pages


# ── STEP 2: Split into chunks ───────────────────────────────────
def split_into_chunks(pages):
    """
    Why do we chunk?
    - LLMs have a context limit — can't read 10 pages at once
    - Smaller chunks = more precise retrieval
    - chunk_size=500  : each chunk is ~500 characters
    - chunk_overlap=50: chunks overlap by 50 chars so we
                        don't cut a sentence mid-thought
    """
    print("✂️  Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(pages)
    print(f"✅ Created {len(chunks)} chunks")
    return chunks


# ── STEP 3: Embed + store in ChromaDB ──────────────────────────
def store_in_chromadb(chunks):
    """
    OllamaEmbeddings uses nomic-embed-text locally
    to convert each chunk's text into a vector (list of numbers).

    Chroma.from_documents:
    - Takes all chunks
    - Embeds each one using nomic-embed-text
    - Stores text + vector in ChromaDB
    - persist_directory saves it to disk so it survives restarts
    """
    print("🧠 Embedding chunks and storing in ChromaDB...")

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"),
        collection_name="resume"   # name of our collection inside ChromaDB
    )

    print(f"✅ Stored {len(chunks)} chunks in ChromaDB")
    print(f"📁 ChromaDB saved at: {os.getenv('CHROMA_PERSIST_DIR', './chroma_db')}")
    return vectorstore


# ── MAIN: Run all steps ─────────────────────────────────────────
if __name__ == "__main__":
    pages  = load_resume(RESUME_PATH)
    chunks = split_into_chunks(pages)
    store_in_chromadb(chunks)
    print("\n🎉 Resume ingested successfully! Ready for the agent.")
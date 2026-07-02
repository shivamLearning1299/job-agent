# ── backend/main.py ───────────────────────────────────────────

from dotenv import load_dotenv
load_dotenv("backend/.env")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add backend folder to path so we can import agent.py
sys.path.append(os.path.dirname(__file__))
from agent import analyze_jd

# ── Create FastAPI app ─────────────────────────────────────────
app = FastAPI(
    title="Job Application Agent API",
    description="RAG agent that tailors your resume to any JD",
    version="1.0.0"
)

# ── CORS — allows React (localhost:5173) to call this API ──────
# Without this, browser will block React from calling FastAPI
# It's a security feature — we explicitly whitelist our React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],   # allow GET, POST, etc.
    allow_headers=["*"],   # allow all headers
)

# ── Request model — what React sends us ───────────────────────
# Pydantic automatically validates the incoming JSON
# If "jd_text" is missing → FastAPI returns 422 error automatically
class AnalyzeRequest(BaseModel):
    jd_text: str  # the job description text

# ── Response model — what we send back to React ───────────────
class AnalyzeResponse(BaseModel):
    result: str        # the tailored bullets + skill gaps
    chunks_used: int   # how many resume chunks were retrieved

# ── Routes ────────────────────────────────────────────────────

# Health check — useful to test if server is running
@app.get("/")
def root():
    return {"status": "running", "message": "Job Agent API is live!"}

# Main endpoint — React calls this with the JD text
@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    """
    Takes a job description, runs the RAG agent,
    returns tailored bullets and skill gaps.
    """
    # Validate input isn't empty
    if not request.jd_text.strip():
        raise HTTPException(
            status_code=400,
            detail="JD text cannot be empty"
        )

    try:
        print(f"\n📥 Received JD ({len(request.jd_text)} chars)")

        # Call our agent — same function from agent.py
        result = analyze_jd(request.jd_text)

        return AnalyzeResponse(
            result=result,
            chunks_used=4
        )

    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
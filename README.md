# Job Application Agent 🤖

A full-stack AI application that uses RAG (Retrieval Augmented Generation) to analyze job descriptions and tailor your resume accordingly.

## Project Structure

```
├── backend/           # FastAPI + LangChain RAG agent
├── frontend/          # React + Vite + Tailwind UI
├── chroma_db/         # Vector database for embeddings
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Tech Stack

### Backend
- **FastAPI** - REST API server
- **LangChain** - LLM orchestration & RAG
- **ChromaDB** - Vector database for semantic search
- **Ollama** - Local LLM inference
- **LangFuse** - LLM observability & debugging
- **PyPDF** - PDF processing for resumes

### Frontend
- **React 19** - UI framework
- **Vite** - Fast build tool & dev server
- **Tailwind CSS** - Utility-first styling
- **TypeScript ready** - Vite setup supports TS

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Ollama (for local LLM)

### Backend Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Create .env file
cp backend/.env.example backend/.env  # (if available)

# Run API server
uvicorn backend.main:app --reload
# API runs at http://localhost:8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# Frontend runs at http://localhost:5173
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `POST /analyze` | POST | Analyze JD and return tailored resume |

See `backend/main.py` for full API documentation.

## Environment Variables

**Backend** (`.env` in `backend/` folder):
```
OLLAMA_MODEL=your_model_name
LANGFUSE_PUBLIC_KEY=your_key
LANGFUSE_SECRET_KEY=your_secret
```

## Development Commands

**Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev      # Development server
npm run build    # Production build
npm run lint     # Run linter
npm run preview  # Preview production build
```

## Project Status
🚧 In active development

## Next Steps
- [ ] Add authentication
- [ ] Implement job description parsing
- [ ] Add resume upload/download features
- [ ] Deploy to production

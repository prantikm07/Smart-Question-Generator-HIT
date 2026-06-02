# Smart Question Generator — HIT

AI-powered exam paper generator for Haldia Institute of Technology. Upload subject PDFs, get structured question papers instantly.

## Stack
- **Frontend:** Vanilla HTML/CSS/JS (Live Server)
- **Backend:** Python Flask + LangChain + Groq (LLaMA 3.1)
- **Vector DB:** ChromaDB + SentenceTransformers
- **PDF:** ReportLab (server-side)

## Project Structure
```
├── backend/
│   ├── app.py           # Flask API
│   ├── generator.py     # Groq AI question generator
│   ├── retriever.py     # ChromaDB vector search
│   ├── requirements.txt
│   └── vector_store/    # Generated after running notebook
├── data/
│   ├── DBMS/
│   ├── DSA/
│   ├── OOPS/
│   ├── OS/
│   └── SE/
├── frontend/
│   └── index.html
└── notebook/
    └── GenerateDB.ipynb  # Run once to build vector store
```

## Setup

**1. Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**2. Add your PDFs**  
Drop PDFs into the relevant folder under `data/` (DBMS, DSA, OOPS, OS, SE).

**3. Build the vector store** (run once, or when PDFs change)  
Open and run `notebook/GenerateDB.ipynb`

**4. Start the backend**
```bash
cd backend
python app.py
```

**5. Open the frontend**  
Open `frontend/index.html` with VS Code Live Server → `http://127.0.0.1:5500/frontend/index.html`

## API Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/connect` | Health check |
| POST | `/api/generate-paper` | Generate questions (JSON) |
| POST | `/api/generate-pdf` | Generate and download PDF |

## Available Subjects
DBMS · DSA · OOPS · Operating Systems · Software Engineering
# Smart-Question-Generator-HIT

Smart-Question-Generator-HIT/
│
├── backend/                  # Python API Backend
│   ├── app.py                # Main web server entry point (FastAPI or Flask)
│   ├── retriever.py          # Handles local ChromaDB queries
│   ├── generator.py          # Handles Groq API payload generation
│   ├── requirements.txt      # Backend Python dependencies
│   └── vector_store/         # <--- PASTE YOUR EXTRACTED 'db' FOLDER HERE!
│       ├── chroma.sqlite3
│       └── b7da5772-.../
│
├── frontend/                 # Web UI Frontend
│   ├── index.html            # Main webpage layout
│   ├── style.css             # UI styling
│   └── app.js                # Handles API calls to the backend
│
└── data/                     # Optional: Keep a backup copy of your original PDFs
    ├── dbms/
    ├── dsa/
    └── os/
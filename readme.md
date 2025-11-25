🧠 RAG-Buddy
Your Personal AI Assistant Powered by RAG + Local/Gemini Models

RAG-Buddy is a Retrieval-Augmented Generation (RAG) system that supports:

✔ Local LLMs via LM Studio
✔ Cloud LLMs via Google Gemini API
✔ GPU-accelerated embeddings
✔ Multi-PDF ingestion
✔ Topic-based organization
✔ Fast & interactive Streamlit UI

🚀 Features

1. PDF Upload + Auto-Ingestion
Upload one or more PDFs through the frontend.
Documents are auto-converted → chunked → embedded → stored in ChromaDB.

2. Dual Model Support (Toggle)
Choose:
Local LLM via LM Studio
Gemini API

3. Topic Tagging
Assign topics like:
[dbms, maths, ai, networking, etc.]

Queries use topic-specific retrieval for accurate results.

4. Streamlit Frontend

File uploader
Toggle between local/Gemini
Previous chat history
Clean UI
Backend status indicators

5. FastAPI Backend
Endpoints:
/ingest
/query
/list-topics
/health

🏁 Quick Start

1️⃣ Clone the repo

```bash
git clone https://github.com/JatinK3/RAG-Buddy.git
cd RAG-Buddy

2️⃣ Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

NOTE: Create .env
GOOGLE_API_KEY=your_key_here
LMSTUDIO_BASE_URL=http://localhost:1234/v1

Start LM Studio (for local model users)
Load:
Llama-3.1-8B-Instruct (Any model of your choice if you want)

3️⃣ Run backend
cd backend
uvicorn main:app --reload

API available at http://localhost:8000/docs

4️⃣ Run frontend
cd frontend
streamlit run app.py


Switch between Models
Inside config.py
USE_GEMINI = True  # or False to use local LLM


📄 Example Document

Includes a small dummy PDF for testing: 

Upload more PDFs using ingestion endpoint:
POST http://localhost:8000/ingest

⭐ Future Enhancements

Chat history with persistence
Auth & user profiles
Model download manager
Reranking pipeline

📝 License
MIT License – Fully open-source.

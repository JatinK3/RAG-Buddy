from fastapi import FastAPI, UploadFile, Form
from backend.ingest import ingest_pdf, collection
from backend.llm_gemini import ask_gemini
from backend.llm_local import ask_local
from backend.config import USE_GEMINI
from pydantic import BaseModel
import os

app = FastAPI(title="RAG-Buddy API")

class RagRequest(BaseModel):
    question: str
    top_k: int = 3
    topic: str | None = None
    backend: str | None = None  


UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/ingest")
async def upload_and_ingest(file: UploadFile, topic: str = Form("general")):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    pages = ingest_pdf(file_path, topic)
    return {"status": "success", "pages_ingested": pages, "topic": topic, "filename": file.filename}

@app.post("/rag")
async def rag_query(req: RagRequest):
    results = collection.query(
        query_texts=[req.question],
        n_results=req.top_k,
        where={"topic": req.topic} if req.topic else None,
    )

    docs = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n\n".join(docs)

    # Decide which model to use:
    # 1) If frontend sent backend explicitly, use that
    # 2) Otherwise, fall back to USE_GEMINI in config.py
    backend = (req.backend or ("gemini" if USE_GEMINI else "local")).lower()

    if backend == "gemini":
        answer = ask_gemini(req.question, context)
    else:
        answer = ask_local(req.question, context)

    return {
        "answer": answer,
        "sources": metadatas,
    }

@app.get("/topics")
def list_topics():
    results = collection.get(include=["metadatas"])
    topics = sorted({meta["topic"] for meta in results["metadatas"]})
    return {"topics": topics}
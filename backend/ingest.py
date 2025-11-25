# backend/ingest.py

import os
import chromadb
from PyPDF2 import PdfReader
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Where to store Chroma DB (relative to this file)
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
os.makedirs(DB_DIR, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=DB_DIR)
embedding_function = SentenceTransformerEmbeddingFunction()

collection = chroma_client.get_or_create_collection(
    name="rag-buddy",
    embedding_function=embedding_function,
    metadata={"hnsw:space": "cosine"},
)


def ingest_pdf(file_path: str, topic: str = "general") -> int:
    """
    Read a PDF, embed all pages in a batch, and store them in ChromaDB.
    Returns number of pages ingested.
    """
    reader = PdfReader(file_path)
    pages_text = []
    metadatas = []
    ids = []

    filename = os.path.basename(file_path)

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        text = text.strip()
        if not text:
            continue

        pages_text.append(text)
        metadatas.append({"page": i, "topic": topic, "source": filename})
        ids.append(f"{filename}-page-{i}")

    if not pages_text:
        return 0

    # ⚡ Batch embeddings in one go
    embeddings = embedding_function(pages_text)

    collection.add(
        documents=pages_text,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings,
    )

    return len(pages_text)

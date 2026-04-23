from fastapi import FastAPI
from app.api.routes import router
from app.vectorstore.faiss_db import FAISSDB
from app.ingestion.loader import load_documents
from app.chunking.chunker import chunk_data
from app.embedding.embedder import get_embeddings

app = FastAPI()

# Load pipeline at startup
documents = load_documents("data/")
chunks = chunk_data(documents)

texts = [doc.page_content for doc in chunks]
embeddings = get_embeddings(texts)

db = FAISSDB(dim=len(embeddings[0]))
db.add(embeddings, texts)

# inject db into routes
import app.api.routes as routes
routes.db = db

app.include_router(router)
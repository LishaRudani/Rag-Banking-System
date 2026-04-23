from app.embedding.embedder import get_embeddings

def retrieve(query, db):
    query_embedding = get_embeddings([query])[0]
    chunks, scores = db.search(query_embedding, k=3)
    return chunks, scores
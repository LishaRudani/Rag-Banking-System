from fastapi import APIRouter
from app.retrieval.retriever import retrieve
from app.llm.generator import generate_answer
from app.hallucination.detector import detect_hallucination
from app.kb.token import generate_token
from app.kb.kb_service import fetch_from_kb

router = APIRouter()

db = None  # will be injected from main.py


# ✅ MAIN QUERY API
@router.post("/query")
def query_api(query: str):
    print("Query:", query)

    chunks, scores = retrieve(query, db)
    print("Chunks:", chunks)

    if not chunks:
        return {"error": "No relevant data found"}

    context = " ".join(chunks)

    answer = generate_answer(query, context)
    print("Answer:", answer)

    # ✅ hallucination check
    if detect_hallucination(answer, context):
        print("Hallucination detected")

        token = generate_token()
        kb_data = fetch_from_kb(token, query)

        return {
            "source": "KB",
            "answer": kb_data
        }

    return {
        "source": "RAG",
        "answer": answer,
        "context_used": chunks
    }


# ✅ DEBUG API (VERY IMPORTANT)
@router.post("/query/debug")
def query_debug(query: str):
    chunks, scores = retrieve(query, db)
    context = " ".join(chunks)

    answer = generate_answer(query, context)
    hallucination = detect_hallucination(answer, context)

    return {
        "query": query,
        "chunks": chunks,
        "scores": scores.tolist() if hasattr(scores, "tolist") else scores,
        "context": context,
        "answer": answer,
        "hallucination": hallucination
    }


# ✅ KB TOKEN API
@router.get("/kb/token")
def get_token():
    return {"token": generate_token()}


# ✅ KB FETCH API
@router.post("/kb/fetch")
def kb_fetch(query: str, token: str):
    data = fetch_from_kb(token, query)
    return {"data": data}


# ✅ HEALTH CHECK
@router.get("/health")
def health():
    return {"status": "running"}
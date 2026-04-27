import os
from sentence_transformers import SentenceTransformer
import numpy as np
from app.llm_client import ask_llm

model = SentenceTransformer("all-MiniLM-L6-v2")

DOCUMENTS = []

def index_document(text: str):
    chunks = text.split("\n")
    for chunk in chunks:
        if len(chunk.strip()) > 20:
            embedding = model.encode(chunk)
            DOCUMENTS.append((chunk, embedding))

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def query_rag(question: str) -> str:
    if not DOCUMENTS:
        return "No documents indexed."

    q_emb = model.encode(question)

    scores = []
    for chunk, emb in DOCUMENTS:
        score = cosine(q_emb, emb)
        scores.append((score, chunk))

    scores.sort(reverse=True)
    top_chunks = [c for _, c in scores[:3]]

    context = "\n".join(top_chunks)

    prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{question}
"""

    return ask_llm(prompt)
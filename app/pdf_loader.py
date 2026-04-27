import pdfplumber
import os
from app.config import UPLOAD_DIR

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def load_pdf(file_path: str) -> dict:
    filename = os.path.basename(file_path)
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    return {
        "filename": filename,
        "full_text": text,
        "chunks": chunks,
        "num_chunks": len(chunks)
    }
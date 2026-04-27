from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_KEY
from datetime import datetime

client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_document_metadata(filename: str, num_chunks: int):
    try:
        client.table("documents").insert({
            "filename": filename,
            "num_chunks": num_chunks,
            "upload_date": datetime.now().isoformat(),
            "status": "indexed"
        }).execute()
    except Exception as e:
        print(f"Supabase error: {e}")

def get_all_documents():
    try:
        result = client.table("documents").select("*").order("upload_date", desc=True).execute()
        return result.data
    except Exception as e:
        print(f"Supabase error: {e}")
        return []

def document_exists(filename: str) -> bool:
    try:
        result = client.table("documents").select("id").eq("filename", filename).execute()
        return len(result.data) > 0
    except Exception as e:
        print(f"Supabase error: {e}")
        return False
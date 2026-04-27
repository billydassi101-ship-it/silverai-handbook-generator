import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.0-flash")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

UPLOAD_DIR = "data/uploads"
OUTPUT_DIR = "data/outputs"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") 
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

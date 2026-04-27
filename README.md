# 🚀 SilverAI Handbook Generator

An AI-powered application that allows users to upload PDFs, chat with them, and generate structured handbooks from their content.

---

## 📌 Features

- 📄 Upload PDF documents  
- 🧠 Index content using LightRAG (RAG system)  
- 💬 Chat with documents (context-aware responses)  
- 📖 Generate structured handbook from uploaded PDFs  
- 🗄️ Store document metadata using Supabase  

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit  
- **LLM**: Groq (LLaMA 3.3)  
- **RAG**: LightRAG  
- **Embeddings**: SentenceTransformers  
- **Database**: Supabase (metadata storage)  
- **PDF Processing**: PyPDF / pdfplumber  

---

## ⚙️ Setup

### 1. Clone repo

git clone https://github.com/billydassi101-ship-it/silverai-handbook-generator.git  
cd silverai-handbook-generator  

### 2. Install dependencies

pip install -r requirements.txt  

### 3. Configure environment variables

Create a `.env` file:

GROQ_API_KEY=your_key_here  
SUPABASE_URL=your_url_here  
SUPABASE_KEY=your_key_here  

---

## ▶️ Run the app

streamlit run app/main.py  

---

##  How it works

1. Upload PDF → text extraction  
2. Text chunking → embeddings  
3. LightRAG builds knowledge context  
4. User asks questions → relevant context retrieved  
5. LLM generates answers or handbook  

---

## 📬 Submission Includes

- Working application  
- GitHub repository  
- Demo video  
- Write-up summary  

---

## ⚠️ Notes

- Supabase is used to store document metadata (filename, chunks, status)  
- Local storage is used for embeddings (simplified architecture)  
- Token limits may affect long handbook generation  

---

## 👤 Author

Made With ❤️ By Billy_Dassi

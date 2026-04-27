import sys
import os

# Permet à Streamlit de retrouver le package app/ quand on lance app/main.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from app.pdf_loader import load_pdf
from app.rag_engine import index_document, query_rag
from app.handbook_generator import generate_handbook
from app.config import UPLOAD_DIR, OUTPUT_DIR
from app.utils import save_document_metadata, document_exists, get_all_documents

# Création des dossiers si besoin
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configuration de la page
st.set_page_config(page_title="SilverAI Handbook Generator", layout="wide")
st.title("📚 SilverAI Handbook Generator")
st.markdown("Upload PDFs, chat with them, and generate comprehensive handbooks.")

# Initialisation des variables de session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []

if "full_context" not in st.session_state:
    st.session_state.full_context = ""

if "rag_ready" not in st.session_state:
    st.session_state.rag_ready = False


# Sidebar : upload et indexation des PDF
with st.sidebar:
    st.header("📄 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("🔄 Index PDFs", type="primary"):
            for uploaded_file in uploaded_files:

                # Vérifie si le fichier est déjà indexé localement ou enregistré dans Supabase
                if (
                    uploaded_file.name in st.session_state.indexed_files
                    or document_exists(uploaded_file.name)
                ):
                    st.info(f"{uploaded_file.name} already indexed.")
                    continue

                with st.spinner(f"Processing {uploaded_file.name}..."):

                    # Sauvegarde temporaire du PDF uploadé
                    tmp_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

                    with open(tmp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Extraction du texte et découpage en chunks
                    result = load_pdf(tmp_path)

                    # Indexation dans le moteur RAG local
                    index_document(result["full_text"])

                    # Sauvegarde des métadonnées dans Supabase
                    save_document_metadata(
                        filename=uploaded_file.name,
                        num_chunks=result["num_chunks"]
                    )

                    # Mise à jour de l’état local Streamlit
                    st.session_state.indexed_files.append(uploaded_file.name)
                    st.session_state.full_context += result["full_text"] + "\n\n"
                    st.session_state.rag_ready = True

                    st.success(f"✅ {uploaded_file.name} indexed!")

    # Permet d’utiliser un index déjà existant
    if not st.session_state.rag_ready:
        if st.button("📂 Use existing index"):
            st.session_state.rag_ready = True
            st.success("✅ Existing index loaded!")

    # Affichage des fichiers indexés pendant la session
    if st.session_state.indexed_files:
        st.markdown("**Indexed files in current session:**")
        for filename in st.session_state.indexed_files:
            st.markdown(f"- {filename}")

    # Affichage des documents enregistrés dans Supabase
    st.markdown("**Documents stored in Supabase:**")
    documents = get_all_documents()

    if documents:
        for doc in documents:
            st.markdown(
                f"- {doc['filename']} ({doc['num_chunks']} chunks) - {doc['status']}"
            )
    else:
        st.caption("No document metadata found in Supabase.")


# Onglets principaux
tab1, tab2 = st.tabs(["💬 Chat", "📖 Generate Handbook"])


# Onglet Chat
with tab1:
    st.header("Chat with your documents")

    # Affichage de l’historique de conversation
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Champ de question utilisateur
    if prompt := st.chat_input("Ask a question about your documents..."):

        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if not st.session_state.rag_ready:
                response = "Please upload and index PDFs first."
            else:
                with st.spinner("Thinking..."):
                    try:
                        # Recherche dans les documents indexés + réponse LLM
                        response = query_rag(prompt)

                        if not response or "[no-context]" in response:
                            response = "I couldn't find relevant information. Try rephrasing."

                    except Exception as e:
                        response = f"Error: {str(e)}"

            st.markdown(response)

            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )


# Onglet Handbook
with tab2:
    st.header("Generate a Comprehensive Handbook")

    topic = st.text_input(
        "Handbook topic:",
        placeholder="e.g., Retrieval-Augmented Generation"
    )

    if st.button("📝 Generate Handbook", type="primary"):

        if not st.session_state.rag_ready:
            st.error("Please index PDFs first.")

        elif not topic:
            st.error("Please enter a topic.")

        else:
            with st.spinner("Generating handbook... this may take several minutes."):
                try:
                    # Génération du handbook à partir du contexte extrait des PDF
                    handbook = generate_handbook(
                        topic,
                        st.session_state.full_context
                    )

                    st.success(
                        f"✅ Handbook generated! ({len(handbook.split())} words)"
                    )

                    output_path = os.path.join(OUTPUT_DIR, "handbook.md")

                    # Lecture du fichier généré pour téléchargement
                    with open(output_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    st.download_button(
                        label="⬇️ Download Handbook",
                        data=content,
                        file_name="handbook.md",
                        mime="text/markdown"
                    )

                    # Aperçu limité du handbook dans l’interface
                    st.markdown(handbook[:3000] + "...")

                except Exception as e:
                    st.error(f"Error: {str(e)}")
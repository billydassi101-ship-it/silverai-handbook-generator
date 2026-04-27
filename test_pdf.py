import asyncio
from app.pdf_loader import load_pdf
from app.rag_engine import get_rag
from lightrag import QueryParam

async def main():
    result = load_pdf('data/uploads/user_manuel.pdf')
    print(f"PDF chargé : {result['num_chunks']} chunks")

    print("Indexation en cours...")
    rag = await get_rag()
    await rag.ainsert(result['full_text'])
    print("Indexation terminée !")

    question = "De quoi parle ce document ?"
    print(f"\nQuestion : {question}")
    reponse = await rag.aquery(question, param=QueryParam(mode="hybrid"))
    print(f"Réponse : {reponse}")

asyncio.run(main())
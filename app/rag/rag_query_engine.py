import numpy as np
from app.rag.embedder import get_embeddings_batch
from app.rag.generator import generate_answer
from app.rag.retriever import retrieve_top_k



def rag_query(question: str, vectorstore, top_k: int = 5):
    """
    Full RAG pipeline:
    1. Embed question
    2. Vector search (using the passed vectorstore)
    3. Build context
    4. Generate final answer
    """

    print(f"[RAG] Query received: {question}")

    question_embedding = get_embeddings_batch([question])[0].reshape(1, -1)

   
    
    top_chunks = retrieve_top_k(question_embedding, vectorstore, top_k=top_k)

    context = "\n\n".join([c["text"] for c in top_chunks])

    sources = [f"chunk_{c['chunk_id']}" for c in top_chunks]

    answer = generate_answer(question, context)

    return answer, sources
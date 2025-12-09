import os
from app.pipeline.scraper import scrape_cloudwalk
from app.pipeline.cleaner import clean_and_save
from app.pipeline.chunker import chunk_text
from app.rag.embedder import get_embeddings_batch
from app.rag.vectorstore import VectorStore


BATCH_SIZE = 32   


def build_vector_index():

    print("\n=== 📌 STEP 1: Scraping CloudWalk Website ===")
    texts = scrape_cloudwalk()

    print("\n=== 📌 STEP 2: Cleaning Text ===")
    cleaned_texts = []
    for i, text in enumerate(texts):
        filename = f"page_{i}.txt"
        cleaned = clean_and_save(text, filename)
        cleaned_texts.append(cleaned)

    print("\n=== 📌 STEP 3: Chunking ===")
    all_chunks = []
    for cleaned in cleaned_texts:
        chunks = chunk_text(cleaned)
        all_chunks.extend(chunks)

    print(f"[CHUNKER] Total chunks created: {len(all_chunks)}")

    print("\n=== 📌 STEP 4: Embedding Chunks (BATCH MODE) ===")

    # Get sample embedding dimension
    sample_emb = get_embeddings_batch(["test text"])[0]
    dim = len(sample_emb)

    vs = VectorStore(dim)

    total = len(all_chunks)
    for start in range(0, total, BATCH_SIZE):
        batch = all_chunks[start:start + BATCH_SIZE]

        embeddings = get_embeddings_batch(batch)

        for i, emb in enumerate(embeddings):
            chunk_index = start + i
            vs.add(
                emb,
                {
                    "chunk_id": chunk_index,
                    "text": batch[i]
                }
            )

        print(f"[BATCH] Embedded {min(start + BATCH_SIZE, total)}/{total}")

    print("\n=== 📌 STEP 5: Saving Vector Store ===")
    vs.save()

    print("\n🎉 DONE! Vector Index Successfully Built with Batching.\n")


if __name__ == "__main__":
    build_vector_index()

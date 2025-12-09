import numpy as np


def retrieve_top_k(query_embedding: np.ndarray, vectorstore, top_k=5):
    """
    Returns metadata of top-k most similar chunks.
    """
    distances, indices = vectorstore.index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        meta = vectorstore.metadata[idx]
        results.append(meta)

    return results

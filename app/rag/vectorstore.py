import faiss
import numpy as np
import json
import os


class VectorStore:
    def __init__(
        self,
        dim,
        index_path="data/vectorstore/faiss.index",
        metadata_path="data/vectorstore/metadata.json"
    ):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

        self.index_path = index_path
        self.metadata_path = metadata_path

    def add(self, vector, metadata):
        """
        Add one embedding + metadata.
        `vector` is 1D list/array.
        """
        vector = np.array(vector, dtype="float32").reshape(1, -1)
        self.index.add(vector)
        self.metadata.append(metadata)

    def search(self, query_vector, top_k=5):
        """
        query_vector: 1D embedding
        """
        query_vector = np.array(query_vector, dtype="float32").reshape(1, -1)
        distances, idx = self.index.search(query_vector, top_k)
        results = []

        for i, dist in zip(idx[0], distances[0]):
            if i < len(self.metadata):
                results.append({
                    "metadata": self.metadata[i],
                    "distance": float(dist)
                })

        return results

    def save(self):
        """
        Save FAISS index + metadata.
        """
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

        faiss.write_index(self.index, self.index_path)

        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

        print(f"[SAVE] Index saved → {self.index_path}")
        print(f"[SAVE] Metadata saved → {self.metadata_path}")

    def load(self):
        """
        Load index + metadata.
        """
        self.index = faiss.read_index(self.index_path)

        with open(self.metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        print("[LOAD] Vector index & metadata loaded")

import os
import numpy as np
import requests
from app.config import OPENROUTER_API_KEY


def get_embeddings_batch(text_list):
    """Embed a batch of texts using OpenRouter thenlper/gte-base."""
    url = "https://openrouter.ai/api/v1/embeddings"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "thenlper/gte-base",
        "input": text_list
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Embedding API Error {response.status_code}: {response.text}")

    data = response.json()["data"]

    return [np.array(item["embedding"], dtype="float32") for item in data]

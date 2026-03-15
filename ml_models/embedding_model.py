"""
Embedding Model: Generates text embeddings using sentence-transformers all-MiniLM-L6-v2
"""
import numpy as np
from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    """Lazy-load the model to avoid startup delay."""
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def generate_embedding(text: str) -> list:
    """Generate a sentence embedding for the given text."""
    model = get_model()
    if not text or not text.strip():
        return []
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


def generate_batch_embeddings(texts: list) -> list:
    """Generate embeddings for a list of texts."""
    model = get_model()
    if not texts:
        return []
    embeddings = model.encode(texts, convert_to_numpy=True, batch_size=16)
    return embeddings.tolist()

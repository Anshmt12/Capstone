"""HuggingFace embeddings for legal documents."""
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings

# Cache embeddings instance
_embeddings = None


def get_embeddings() -> HuggingFaceEmbeddings:
    """Get the embedding model (downloads on first use, then cached)."""
    global _embeddings
    
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    
    return _embeddings
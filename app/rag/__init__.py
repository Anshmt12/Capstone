"""RAG module using ChromaDB for vector storage."""
from app.rag.embeddings import get_embeddings
from app.rag.vector_store import (
    get_vector_store,
    add_documents,
    similarity_search,
    get_collection_stats,
)
from app.rag.retriever import LegalRetriever, get_legal_retriever

__all__ = [
    "get_embeddings",
    "get_vector_store",
    "add_documents",
    "similarity_search",
    "get_collection_stats",
    "LegalRetriever",
    "get_legal_retriever",
]
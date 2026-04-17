"""ChromaDB-based vector store for legal documents - No PostgreSQL needed!"""
import os
import logging
from langchain_chroma import Chroma
from app.config import settings
from app.rag.embeddings import get_embeddings

logger = logging.getLogger(__name__)

COLLECTION_NAME = "legal_documents"
CHROMA_PERSIST_DIR = "data/chroma_db"

# Cache the vector store instance
_vector_store = None


def get_vector_store() -> Chroma:
    """Get or create the ChromaDB store."""
    global _vector_store
    
    if _vector_store is None:
        # Ensure directory exists
        os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
        
        _vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=get_embeddings(),
            persist_directory=CHROMA_PERSIST_DIR,
        )
        logger.info(f"ChromaDB initialized at {CHROMA_PERSIST_DIR}")
    
    return _vector_store


def add_documents(texts: list[str], metadatas: list[dict] = None):
    """Add documents to the vector store."""
    store = get_vector_store()
    
    if metadatas is None:
        metadatas = [{}] * len(texts)
    
    # Generate unique IDs for documents
    existing_count = store._collection.count()
    ids = [f"doc_{existing_count + i}" for i in range(len(texts))]
    
    store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
    logger.info(f"Added {len(texts)} documents to vector store")


def similarity_search(query: str, k: int = None):
    """Search for similar documents with scores."""
    store = get_vector_store()
    return store.similarity_search_with_score(query, k=k or settings.TOP_K)


def similarity_search_simple(query: str, k: int = None):
    """Search for similar documents without scores."""
    store = get_vector_store()
    return store.similarity_search(query, k=k or settings.TOP_K)


def get_retriever(k: int = None):
    """Get a LangChain retriever."""
    store = get_vector_store()
    return store.as_retriever(search_kwargs={"k": k or settings.TOP_K})


def get_collection_stats() -> dict:
    """Get statistics about the collection."""
    store = get_vector_store()
    return {
        "name": COLLECTION_NAME,
        "count": store._collection.count(),
        "persist_directory": CHROMA_PERSIST_DIR,
    }


def delete_collection():
    """Delete all documents from the collection."""
    global _vector_store
    if _vector_store is not None:
        _vector_store.delete_collection()
        _vector_store = None
        logger.info("Collection deleted")
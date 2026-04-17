"""Configuration for AI Legal Co-Counsel."""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM Providers (free tiers)
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = "meta-llama/llama-3.1-8b-instruct:free"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    HF_API_KEY: str = os.getenv("HF_API_KEY", "")

    # LLM selection: "openrouter", "groq", or "huggingface"
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")

    # Embeddings
    EMBEDDING_MODEL: str = "BAAI/bge-base-en-v1.5"

    # ChromaDB (replaces PostgreSQL - no setup needed!)
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "data/chroma_db")

    # SQLite for case data
    SQLITE_DB: str = os.getenv("SQLITE_DB", "data/cases.db")

    # Upload directory
    UPLOAD_DIR: str = "data/uploads"

    # RAG settings - reduced for free tier limits
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    TOP_K: int = 3  # Reduced from 5 to save tokens

    # MCP
    MCP_PORT: int = int(os.getenv("MCP_PORT", "8001"))

    class Config:
        env_file = ".env"


settings = Settings()
"""LangChain retriever backed by ChromaDB."""
from typing import List, Optional
from langchain_core.retrievers import BaseRetriever, Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from pydantic import Field
from app.rag.vector_store import get_vector_store
from app.config import settings


class LegalRetriever(BaseRetriever):
    """Custom retriever that only returns Indian legal sources."""
    k: int = Field(default_factory=lambda: settings.TOP_K)

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(
        self, 
        query: str,
        *,
        run_manager: Optional[CallbackManagerForRetrieverRun] = None
    ) -> List[Document]:
        """Internal method to get relevant documents."""
        store = get_vector_store()
        results = store.similarity_search_with_score(query, k=self.k)
        
        # Filter: only keep Indian law documents (no foreign precedents)
        docs = []
        for doc, score in results:
            source = (doc.metadata.get("source", "") or "").lower()
            # Exclude explicitly foreign sources
            if any(x in source for x in ["us_", "uk_", "australian_", "canadian_"]):
                continue
            # ChromaDB returns distance (lower = better), convert to similarity
            doc.metadata["relevance_score"] = round(1.0 - float(score), 4)
            docs.append(doc)
        return docs

    async def _aget_relevant_documents(
        self,
        query: str,
        *,
        run_manager: Optional[CallbackManagerForRetrieverRun] = None
    ) -> List[Document]:
        """Async version - just calls sync version."""
        return self._get_relevant_documents(query, run_manager=run_manager)

    def get_relevant_documents(self, query: str) -> List[Document]:
        """Public method for getting relevant documents (LangChain compatibility)."""
        return self._get_relevant_documents(query)

    def invoke(self, query: str, config=None) -> List[Document]:
        """Invoke method for newer LangChain versions."""
        return self._get_relevant_documents(query)


def get_legal_retriever(k: int = None) -> LegalRetriever:
    """Factory function to create a LegalRetriever."""
    return LegalRetriever(k=k or settings.TOP_K)
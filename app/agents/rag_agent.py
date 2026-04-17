"""RAG Agent - retrieves legal documents and generates cited answers."""
import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.agents.llm_provider import get_llm
from app.rag.retriever import LegalRetriever

logger = logging.getLogger(__name__)

RAG_PROMPT = ChatPromptTemplate.from_template("""You are an AI Legal Co-Counsel specializing in Indian law.
Answer the question based ONLY on the provided context from Indian legal sources.
Always cite the specific source (article, section, case name) for every claim.
If the context doesn't contain enough information, say so clearly.
NEVER cite foreign (non-Indian) law or precedents.

Context:
{context}

Question: {question}

Provide a well-structured answer with proper legal citations:""")


def format_docs(docs):
    """Format retrieved documents for the prompt."""
    formatted = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "")
        score = doc.metadata.get("relevance_score", "")
        header = f"[Source {i+1}: {source}"
        if page:
            header += f", Page {page}"
        if score:
            header += f", Score: {score}"
        header += "]"
        formatted.append(f"{header}\n{doc.page_content}")
    return "\n\n---\n\n".join(formatted)


class RAGAgent:
    """RAG-based legal research agent."""

    def __init__(self):
        self.retriever = LegalRetriever()
        self.llm = get_llm(temperature=0.2)
        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | RAG_PROMPT
            | self.llm
            | StrOutputParser()
        )

    def query(self, question: str) -> dict:
        """Run a legal research query."""
        # Get retrieved docs for citation tracking
        docs = self.retriever.get_relevant_documents(question)
        answer = self.chain.invoke(question)
        sources = [
            {
                "source": d.metadata.get("source", "Unknown"),
                "page": d.metadata.get("page"),
                "score": d.metadata.get("relevance_score"),
                "excerpt": d.page_content[:200],
            }
            for d in docs
        ]
        return {"answer": answer, "sources": sources, "query": question}

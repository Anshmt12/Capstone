"""Retrieval Guardrails - Validate RAG results before sending to LLM."""
import logging
from typing import List, Tuple
from dataclasses import dataclass
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


@dataclass
class RetrievalGuardrailResult:
    """Result of retrieval guardrail check."""
    passed: bool
    message: str
    filtered_docs: List[Document] = None
    warnings: List[str] = None


# Valid Indian legal sources
VALID_INDIAN_SOURCES = [
    "constitution of india",
    "supreme court of india",
    "high court",
    "indian penal code",
    "ipc",
    "crpc",
    "code of criminal procedure",
    "code of civil procedure",
    "cpc",
    "indian contract act",
    "indian evidence act",
    "arbitration and conciliation act",
    "companies act",
    "income tax act",
    "gst",
    "consumer protection act",
    "right to information",
    "rti",
    "posh",
    "sexual harassment",
    "motor vehicles act",
    "negotiable instruments act",
    "indian kanoon",
    "scc online",
    "manupatra",
    "air",  # All India Reporter
    "scr",  # Supreme Court Reports
]

# Foreign sources to exclude
FOREIGN_SOURCES = [
    "us_",
    "uk_",
    "us supreme court",
    "uk supreme court",
    "australian",
    "canadian",
    "american",
    "british",
    "european court",
    "echr",
    "9th circuit",
    "federal court",
]


def check_source_validity(doc: Document) -> Tuple[bool, str]:
    """Check if document source is valid Indian law."""
    source = (doc.metadata.get("source", "") or "").lower()
    content = doc.page_content.lower()[:500]  # Check first 500 chars
    
    # Check for foreign sources
    for foreign in FOREIGN_SOURCES:
        if foreign in source or foreign in content:
            return False, f"Foreign source detected: {foreign}"
    
    # Check if it's a known Indian source
    is_indian = any(indian in source or indian in content for indian in VALID_INDIAN_SOURCES)
    
    if not is_indian:
        # Not explicitly Indian, but also not foreign - allow with warning
        return True, "Source not explicitly Indian law, but allowed"
    
    return True, "Valid Indian legal source"


def check_relevance_score(doc: Document, min_score: float = 0.3) -> Tuple[bool, str]:
    """Check if document has sufficient relevance score."""
    score = doc.metadata.get("relevance_score", 0.5)
    
    if score < min_score:
        return False, f"Low relevance score: {score:.2f}"
    
    return True, f"Good relevance: {score:.2f}"


def check_content_quality(doc: Document, min_length: int = 50) -> Tuple[bool, str]:
    """Check if document content meets quality standards."""
    content = doc.page_content.strip()
    
    if len(content) < min_length:
        return False, "Content too short to be useful"
    
    # Check for garbage/corrupted content
    if content.count("�") > 5:  # Unicode replacement characters
        return False, "Corrupted content detected"
    
    # Check for excessive repetition
    words = content.split()
    if len(words) > 10:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.3:
            return False, "Excessive repetition in content"
    
    return True, "Content quality OK"


def check_citation_present(doc: Document) -> Tuple[bool, str]:
    """Check if document has proper citation/reference."""
    metadata = doc.metadata
    
    has_citation = any([
        metadata.get("citation"),
        metadata.get("case_name"),
        metadata.get("article"),
        metadata.get("section"),
        metadata.get("source"),
    ])
    
    if not has_citation:
        return True, "No citation metadata (warning)"  # Warning, not failure
    
    return True, "Citation present"


def validate_retrieval(documents: List[Document], min_docs: int = 1) -> RetrievalGuardrailResult:
    """
    Main retrieval validation function.
    
    Args:
        documents: List of retrieved documents
        min_docs: Minimum number of valid documents required
    
    Returns:
        RetrievalGuardrailResult with filtered documents
    """
    if not documents:
        return RetrievalGuardrailResult(
            passed=False,
            message="No relevant legal documents found. Please try rephrasing your question.",
            filtered_docs=[],
            warnings=["Empty retrieval"]
        )
    
    filtered_docs = []
    warnings = []
    
    for i, doc in enumerate(documents):
        doc_warnings = []
        is_valid = True
        
        # Run all checks
        source_valid, source_msg = check_source_validity(doc)
        if not source_valid:
            logger.info(f"Doc {i} failed source check: {source_msg}")
            is_valid = False
            continue
        elif "warning" in source_msg.lower():
            doc_warnings.append(source_msg)
        
        relevance_valid, relevance_msg = check_relevance_score(doc)
        if not relevance_valid:
            logger.info(f"Doc {i} failed relevance check: {relevance_msg}")
            is_valid = False
            continue
        
        quality_valid, quality_msg = check_content_quality(doc)
        if not quality_valid:
            logger.info(f"Doc {i} failed quality check: {quality_msg}")
            is_valid = False
            continue
        
        citation_valid, citation_msg = check_citation_present(doc)
        if "warning" in citation_msg.lower():
            doc_warnings.append(citation_msg)
        
        if is_valid:
            filtered_docs.append(doc)
            warnings.extend(doc_warnings)
    
    if len(filtered_docs) < min_docs:
        return RetrievalGuardrailResult(
            passed=False,
            message="Could not find enough relevant Indian legal sources. Please refine your query.",
            filtered_docs=filtered_docs,
            warnings=warnings
        )
    
    logger.info(f"Retrieval guardrails passed: {len(filtered_docs)}/{len(documents)} docs retained")
    
    return RetrievalGuardrailResult(
        passed=True,
        message=f"Found {len(filtered_docs)} relevant legal documents",
        filtered_docs=filtered_docs,
        warnings=warnings if warnings else None
    )


def format_docs_for_context(documents: List[Document], max_tokens: int = 2000) -> str:
    """Format filtered documents for LLM context with token limit."""
    context_parts = []
    estimated_tokens = 0
    
    for doc in documents:
        # Rough token estimation: ~4 chars per token
        doc_tokens = len(doc.page_content) // 4
        
        if estimated_tokens + doc_tokens > max_tokens:
            break
        
        # Format document with metadata
        source = doc.metadata.get("source", "Unknown")
        citation = doc.metadata.get("citation", "")
        article = doc.metadata.get("article", "")
        
        header = f"[Source: {source}"
        if citation:
            header += f" | Citation: {citation}"
        if article:
            header += f" | Article: {article}"
        header += "]"
        
        context_parts.append(f"{header}\n{doc.page_content}")
        estimated_tokens += doc_tokens
    
    return "\n\n---\n\n".join(context_parts)


# For direct testing
if __name__ == "__main__":
    # Create test documents
    test_docs = [
        Document(
            page_content="Article 21 of the Constitution of India guarantees right to life and personal liberty.",
            metadata={"source": "Constitution of India", "article": "21", "relevance_score": 0.85}
        ),
        Document(
            page_content="The US Supreme Court held in Miranda v. Arizona...",
            metadata={"source": "US Supreme Court", "relevance_score": 0.75}
        ),
        Document(
            page_content="Short",
            metadata={"source": "Unknown", "relevance_score": 0.9}
        ),
    ]
    
    result = validate_retrieval(test_docs)
    print(f"Passed: {result.passed}")
    print(f"Message: {result.message}")
    print(f"Filtered docs: {len(result.filtered_docs)}")
    print(f"Warnings: {result.warnings}")
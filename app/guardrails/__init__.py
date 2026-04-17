"""
Guardrails Module for AI Legal Co-Counsel

Three-layer guardrail system:
1. Input Guardrail - Validates user queries (jailbreak, PII, off-topic, harmful)
2. Retrieval Guardrail - Validates RAG results (Indian law only, relevance, quality)
3. Output Guardrail - Validates LLM responses (hallucination, citations, harmful advice)
"""

from app.guardrails.input_guardrail import (
    validate_input,
    check_jailbreak,
    check_pii,
    check_off_topic,
    check_harmful_legal,
    GuardrailResult,
)

from app.guardrails.retrieval_guardrail import (
    validate_retrieval,
    check_source_validity,
    check_relevance_score,
    format_docs_for_context,
    RetrievalGuardrailResult,
)

from app.guardrails.output_guardrail import (
    validate_output,
    check_hallucination_indicators,
    check_citation_validity,
    check_harmful_advice,
    ensure_disclaimer,
    OutputGuardrailResult,
)

__all__ = [
    # Input guardrails
    "validate_input",
    "check_jailbreak",
    "check_pii",
    "check_off_topic",
    "check_harmful_legal",
    "GuardrailResult",
    
    # Retrieval guardrails
    "validate_retrieval",
    "check_source_validity",
    "check_relevance_score",
    "format_docs_for_context",
    "RetrievalGuardrailResult",
    
    # Output guardrails
    "validate_output",
    "check_hallucination_indicators",
    "check_citation_validity",
    "check_harmful_advice",
    "ensure_disclaimer",
    "OutputGuardrailResult",
]
"""Output Guardrails - Validate LLM responses before returning to user."""
import re
import logging
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class OutputGuardrailResult:
    """Result of output guardrail check."""
    passed: bool
    message: str
    modified_response: str = None
    issues: List[str] = None
    confidence_score: float = 1.0


# Phrases that indicate hallucination or uncertainty
HALLUCINATION_INDICATORS = [
    r"I (think|believe|assume) (that )?the law (says|states)",
    r"(probably|possibly|maybe|might be|could be) illegal",
    r"I('m| am) not (entirely )?sure (but|if)",
    r"based on my (training|knowledge)",
    r"I don't have (access to|specific|exact) information",
    r"as (far as )?I (know|recall|remember)",
    r"I cannot (find|locate|access) (the|any) (specific|exact)",
]

# Phrases that indicate making up citations
FAKE_CITATION_PATTERNS = [
    r"in the case of .+ v\. .+ \(\d{4}\)",  # Generic case format without specifics
    r"Section \d+ of the .+ Act",  # Generic section reference
    r"Article \d+ states that",  # Without actual constitutional text
]

# Known valid Indian case citation formats
VALID_CITATION_FORMATS = [
    r"\(\d{4}\) \d+ SCC \d+",  # (2017) 10 SCC 1
    r"AIR \d{4} SC \d+",  # AIR 2017 SC 123
    r"\d{4} \(\d+\) SCR \d+",  # 2017 (2) SCR 123
    r"W\.?P\.?\s*\(C\)\s*No\.?\s*\d+",  # Writ Petition numbers
    r"SLP\s*\(C\)\s*No\.?\s*\d+",  # Special Leave Petition
    r"Criminal Appeal No\.?\s*\d+",
    r"Civil Appeal No\.?\s*\d+",
]

# Harmful advice patterns
HARMFUL_ADVICE_PATTERNS = [
    r"you (can|should|could) (safely )?ignore (the )?court",
    r"(don't|do not) (need to )?appear (before|in) court",
    r"you (can|could) (easily )?(bribe|pay off)",
    r"(destroy|hide|conceal|tamper with) (the )?evidence",
    r"(lie|give false testimony|commit perjury)",
    r"(flee|escape|run away) (from|before)",
    r"no (one|court) (will|can) (find out|know)",
]

# Disclaimer to append if not present
LEGAL_DISCLAIMER = "\n\n---\n*Disclaimer: This is AI-generated legal information based on Indian law, not legal advice. Please consult a qualified advocate for specific legal matters.*"


def check_hallucination_indicators(response: str) -> Tuple[bool, List[str]]:
    """Check for phrases indicating potential hallucination."""
    issues = []
    response_lower = response.lower()
    
    for pattern in HALLUCINATION_INDICATORS:
        if re.search(pattern, response_lower):
            issues.append(f"Uncertainty indicator found: '{pattern}'")
    
    # Not a hard fail, but reduces confidence
    return len(issues) == 0, issues


def check_citation_validity(response: str, provided_docs: List[Dict] = None) -> Tuple[bool, List[str]]:
    """
    Check if citations in response are valid.
    
    Args:
        response: LLM response text
        provided_docs: Documents that were provided as context
    """
    issues = []
    
    # Look for citation patterns in response
    citations_found = []
    for pattern in VALID_CITATION_FORMATS:
        matches = re.findall(pattern, response, re.IGNORECASE)
        citations_found.extend(matches)
    
    # If citations are mentioned but none match valid formats
    has_case_mention = bool(re.search(r"\bv\.\s+\w+", response))  # "X v. Y" pattern
    
    if has_case_mention and not citations_found:
        issues.append("Case mentioned without proper citation format")
    
    # Check for fake-looking citations
    for pattern in FAKE_CITATION_PATTERNS:
        if re.search(pattern, response, re.IGNORECASE):
            # Check if this matches a provided document
            is_from_context = False
            if provided_docs:
                for doc in provided_docs:
                    doc_text = str(doc.get("content", "")) + str(doc.get("metadata", {}))
                    if re.search(pattern, doc_text):
                        is_from_context = True
                        break
            
            if not is_from_context:
                issues.append(f"Potentially fabricated citation: {pattern}")
    
    return len(issues) == 0, issues


def check_harmful_advice(response: str) -> Tuple[bool, List[str]]:
    """Check for harmful legal advice."""
    issues = []
    response_lower = response.lower()
    
    for pattern in HARMFUL_ADVICE_PATTERNS:
        if re.search(pattern, response_lower):
            issues.append(f"Harmful advice detected: '{pattern}'")
    
    return len(issues) == 0, issues


def check_response_completeness(response: str, min_length: int = 100) -> Tuple[bool, List[str]]:
    """Check if response is complete and useful."""
    issues = []
    
    if len(response.strip()) < min_length:
        issues.append("Response too short to be useful")
    
    # Check for truncation indicators
    if response.strip().endswith("...") or response.strip().endswith("…"):
        issues.append("Response appears truncated")
    
    # Check for incomplete sentences
    last_char = response.strip()[-1] if response.strip() else ""
    if last_char not in ".!?\"')":
        issues.append("Response may be incomplete")
    
    return len(issues) == 0, issues


def check_disclaimer_present(response: str) -> bool:
    """Check if legal disclaimer is present."""
    disclaimer_keywords = [
        "not legal advice",
        "consult a (qualified )?advocate",
        "consult a (qualified )?lawyer",
        "for informational purposes",
        "ai-generated",
        "disclaimer",
    ]
    
    response_lower = response.lower()
    return any(kw in response_lower for kw in disclaimer_keywords)


def ensure_disclaimer(response: str) -> str:
    """Add disclaimer if not present."""
    if not check_disclaimer_present(response):
        return response + LEGAL_DISCLAIMER
    return response


def check_foreign_law_citation(response: str) -> Tuple[bool, List[str]]:
    """Check if response cites foreign law as binding authority."""
    issues = []
    response_lower = response.lower()
    
    foreign_indicators = [
        (r"under (us|american|uk|british|australian|canadian) law", "Foreign law cited"),
        (r"(us|uk|australian|canadian) supreme court (held|ruled|decided)", "Foreign court cited as authority"),
        (r"according to (us|uk|european) (law|legislation)", "Foreign legislation cited"),
    ]
    
    for pattern, issue_msg in foreign_indicators:
        if re.search(pattern, response_lower):
            # Check if it's comparative context
            comparative_indicators = ["unlike", "in contrast", "compared to", "however in india"]
            is_comparative = any(ind in response_lower for ind in comparative_indicators)
            
            if not is_comparative:
                issues.append(f"{issue_msg} (not as comparative reference)")
    
    return len(issues) == 0, issues


def validate_output(
    response: str,
    provided_docs: List[Dict] = None,
    strict_mode: bool = False
) -> OutputGuardrailResult:
    """
    Main output validation function.
    
    Args:
        response: LLM generated response
        provided_docs: Documents provided as context (for citation verification)
        strict_mode: If True, fail on warnings; if False, only fail on critical issues
    
    Returns:
        OutputGuardrailResult with validation details
    """
    if not response or not response.strip():
        return OutputGuardrailResult(
            passed=False,
            message="Empty response generated",
            issues=["No response content"]
        )
    
    all_issues = []
    confidence = 1.0
    
    # Critical checks (always fail)
    harmful_ok, harmful_issues = check_harmful_advice(response)
    if not harmful_ok:
        return OutputGuardrailResult(
            passed=False,
            message="Response contains potentially harmful legal advice",
            issues=harmful_issues,
            confidence_score=0.0
        )
    
    # Important checks (reduce confidence)
    hallucination_ok, hallucination_issues = check_hallucination_indicators(response)
    if not hallucination_ok:
        all_issues.extend(hallucination_issues)
        confidence -= 0.2 * len(hallucination_issues)
    
    citation_ok, citation_issues = check_citation_validity(response, provided_docs)
    if not citation_ok:
        all_issues.extend(citation_issues)
        confidence -= 0.15 * len(citation_issues)
    
    foreign_ok, foreign_issues = check_foreign_law_citation(response)
    if not foreign_ok:
        all_issues.extend(foreign_issues)
        confidence -= 0.1 * len(foreign_issues)
    
    # Quality checks
    complete_ok, complete_issues = check_response_completeness(response)
    if not complete_ok:
        all_issues.extend(complete_issues)
        confidence -= 0.1 * len(complete_issues)
    
    # Ensure disclaimer
    modified_response = ensure_disclaimer(response)
    
    # Determine pass/fail
    confidence = max(0.0, confidence)
    
    if strict_mode and all_issues:
        return OutputGuardrailResult(
            passed=False,
            message=f"Strict mode: {len(all_issues)} issues found",
            modified_response=modified_response,
            issues=all_issues,
            confidence_score=confidence
        )
    
    # In non-strict mode, pass with warnings
    if confidence < 0.5:
        return OutputGuardrailResult(
            passed=False,
            message="Low confidence in response accuracy",
            modified_response=modified_response,
            issues=all_issues,
            confidence_score=confidence
        )
    
    logger.info(f"Output guardrails passed with confidence {confidence:.2f}")
    
    return OutputGuardrailResult(
        passed=True,
        message="Response validated successfully",
        modified_response=modified_response,
        issues=all_issues if all_issues else None,
        confidence_score=confidence
    )


# For direct testing
if __name__ == "__main__":
    test_responses = [
        "Article 21 guarantees right to life. See K.S. Puttaswamy v. Union of India (2017) 10 SCC 1.",
        "I think the law probably says you can ignore the court summons.",
        "Based on my training, you should destroy the evidence before the hearing.",
        "According to US law, Miranda rights apply here.",
        "Under Article 21 of the Constitution of India, as interpreted in Maneka Gandhi v. Union of India (1978) 1 SCC 248, the right to life includes the right to live with dignity.",
    ]
    
    for resp in test_responses:
        result = validate_output(resp)
        status = "✅ PASS" if result.passed else "❌ FAIL"
        print(f"{status} (conf: {result.confidence_score:.2f}): '{resp[:60]}...'")
        if result.issues:
            print(f"   Issues: {result.issues}")
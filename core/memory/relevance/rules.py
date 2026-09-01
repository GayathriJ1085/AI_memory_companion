from core.memory.extraction.schemas import MemoryCandidate, MemoryType


# These memory types are generally useful for future conversations.
HIGH_VALUE_TYPES = {
    MemoryType.PERSONAL_FACT,
    MemoryType.RELATIONSHIP,
    MemoryType.PREFERENCE,
    MemoryType.ROUTINE,
}


# These words/phrases usually indicate short-lived context.
TEMPORARY_INDICATORS = {
    "today",
    "right now",
    "currently",
    "at the moment",
    "just now",
    "this morning",
    "tonight",
    "yesterday",
    "tomorrow",
}


def calculate_rule_score(candidate: MemoryCandidate) -> float:
    """
    Calculate an initial relevance score using deterministic rules.

    This is intentionally simple. It provides a predictable first
    filtering layer before we introduce AI-based evaluation.
    """

    score = 0.5

    # Long-term memory categories are generally valuable.
    if candidate.type in HIGH_VALUE_TYPES:
        score += 0.30

    # Temporary context is less suitable for long-term memory.
    if candidate.type == MemoryType.TEMPORARY_CONTEXT:
        score -= 0.25

    # Explicit user statements are stronger evidence.
    evidence_name = candidate.evidence_type.value

    if evidence_name == "EXPLICIT_USER_STATEMENT":
        score += 0.10

    # Temporary language lowers relevance.
    text = (
        f"{candidate.content} "
        f"{candidate.source_text}"
    ).lower()

    for indicator in TEMPORARY_INDICATORS:
        if indicator in text:
            score -= 0.15
            break

    return max(0.0, min(1.0, score))
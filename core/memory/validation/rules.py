import re

from core.memory.extraction.schemas import MemoryCandidate


UNCERTAINTY_PATTERNS = [
    r"\bi think\b",
    r"\bmaybe\b",
    r"\bperhaps\b",
    r"\bprobably\b",
    r"\bpossibly\b",
    r"\bmight\b",
    r"\bmay\b",
    r"\bnot sure\b",
    r"\bi guess\b",
]


HYPOTHETICAL_PATTERNS = [
    r"\bif i\b",
    r"\bif we\b",
    r"\bif someday\b",
    r"\bwould\b",
    r"\bcould\b",
    r"\bplanning to\b",
    r"\bplan to\b",
]


NEGATION_PATTERNS = [
    r"\bdon't\b",
    r"\bdo not\b",
    r"\bdoesn't\b",
    r"\bdoes not\b",
    r"\bdidn't\b",
    r"\bdid not\b",
    r"\bnever\b",
    r"\bnot\b",
]


def contains_uncertainty(text: str) -> bool:
    text = text.lower()

    return any(
        re.search(pattern, text)
        for pattern in UNCERTAINTY_PATTERNS
    )


def contains_hypothetical(text: str) -> bool:
    text = text.lower()

    return any(
        re.search(pattern, text)
        for pattern in HYPOTHETICAL_PATTERNS
    )


def contains_negation(text: str) -> bool:
    text = text.lower()

    return any(
        re.search(pattern, text)
        for pattern in NEGATION_PATTERNS
    )


def basic_candidate_checks(
    candidate: MemoryCandidate,
) -> tuple[bool, str]:

    if not candidate.subject.strip():
        return False, "Candidate has an empty subject."

    if not candidate.predicate.strip():
        return False, "Candidate has an empty predicate."

    if not candidate.value.strip():
        return False, "Candidate has an empty value."

    if not candidate.content.strip():
        return False, "Candidate has empty content."

    if not candidate.source_text.strip():
        return False, "Candidate has no source text."

    return True, "Basic candidate fields are valid."
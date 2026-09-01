from core.memory.extraction.schemas import (
    EvidenceType,
    MemoryCandidate,
    MemoryType,
)
from core.memory.validation.models import ValidationDecision
from core.memory.validation.validator import MemoryValidator


def make_candidate(
    content: str,
    source_text: str,
    memory_type: MemoryType = MemoryType.PERSONAL_FACT,
) -> MemoryCandidate:

    return MemoryCandidate(
        type=memory_type,
        subject="user",
        predicate="has",
        value=content,
        content=content,
        evidence_type=EvidenceType.EXPLICIT_USER_STATEMENT,
        source_text=source_text,
    )


def test_valid_explicit_statement():

    candidate = make_candidate(
        content="User likes tea",
        source_text="I like tea.",
    )

    result = MemoryValidator().validate(candidate)

    assert result.decision == ValidationDecision.VALID


def test_uncertain_statement_requires_review():

    candidate = make_candidate(
        content="User likes tea",
        source_text="I think I like tea.",
    )

    result = MemoryValidator().validate(candidate)

    assert result.decision == ValidationDecision.REVIEW


def test_hypothetical_statement_requires_review():

    candidate = make_candidate(
        content="User lives in Chennai",
        source_text="If I move to Chennai, I will live there.",
    )

    result = MemoryValidator().validate(candidate)

    assert result.decision == ValidationDecision.REVIEW


def test_negated_statement_requires_review():

    candidate = make_candidate(
        content="User likes coffee",
        source_text="I do not like coffee.",
    )

    result = MemoryValidator().validate(candidate)

    assert result.decision == ValidationDecision.REVIEW


def test_empty_subject_is_invalid():

    candidate = make_candidate(
        content="User likes tea",
        source_text="I like tea.",
    )

    candidate.subject = ""

    result = MemoryValidator().validate(candidate)

    assert result.decision == ValidationDecision.INVALID


def test_empty_value_is_invalid():

    candidate = make_candidate(
        content="User likes tea",
        source_text="I like tea.",
    )

    candidate.value = ""

    result = MemoryValidator().validate(candidate)

    assert result.decision == ValidationDecision.INVALID


def test_empty_source_text_is_invalid():

    candidate = make_candidate(
        content="User likes tea",
        source_text="I like tea.",
    )

    candidate.source_text = ""

    result = MemoryValidator().validate(candidate)

    assert result.decision == ValidationDecision.INVALID
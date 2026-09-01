from core.memory.conflict.detector import ConflictDetector
from core.memory.conflict.models import ConflictDecision
from core.memory.extraction.schemas import (
    EvidenceType,
    MemoryCandidate,
    MemoryType,
)
from core.memory.models import Memory


def make_candidate(
    subject: str,
    predicate: str,
    value: str,
) -> MemoryCandidate:

    return MemoryCandidate(
        type=MemoryType.PREFERENCE,
        subject=subject,
        predicate=predicate,
        value=value,
        content=f"{subject} {predicate} {value}",
        evidence_type=EvidenceType.EXPLICIT_USER_STATEMENT,
        source_text=f"I {predicate} {value}.",
    )


def make_memory(
    subject: str,
    predicate: str,
    value: str,
) -> Memory:

    return Memory(
        subject=subject,
        predicate=predicate,
        value=value,
        content=f"{subject} {predicate} {value}",
        source_text=f"I {predicate} {value}.",
    )


def test_different_values_with_same_subject_and_predicate_conflict():

    candidate = make_candidate(
        "user",
        "likes",
        "coffee",
    )

    existing = make_memory(
        "user",
        "likes",
        "tea",
    )

    result = ConflictDetector().detect(
        candidate,
        existing,
    )

    assert result.decision == ConflictDecision.CONFLICT
    assert result.existing_memory_id == existing.id


def test_same_value_is_not_a_conflict():

    candidate = make_candidate(
        "user",
        "likes",
        "tea",
    )

    existing = make_memory(
        "user",
        "likes",
        "tea",
    )

    result = ConflictDetector().detect(
        candidate,
        existing,
    )

    assert result.decision == ConflictDecision.NO_CONFLICT


def test_different_predicate_is_not_a_conflict():

    candidate = make_candidate(
        "user",
        "likes",
        "coffee",
    )

    existing = make_memory(
        "user",
        "works_at",
        "Google",
    )

    result = ConflictDetector().detect(
        candidate,
        existing,
    )

    assert result.decision == ConflictDecision.NO_CONFLICT


def test_different_subject_is_not_a_conflict():

    candidate = make_candidate(
        "user",
        "likes",
        "coffee",
    )

    existing = make_memory(
        "Anitha",
        "likes",
        "tea",
    )

    result = ConflictDetector().detect(
        candidate,
        existing,
    )

    assert result.decision == ConflictDecision.NO_CONFLICT


def test_case_difference_does_not_create_false_conflict():

    candidate = make_candidate(
        "USER",
        "LIKES",
        "Coffee",
    )

    existing = make_memory(
        "user",
        "likes",
        "coffee",
    )

    result = ConflictDetector().detect(
        candidate,
        existing,
    )

    assert result.decision == ConflictDecision.NO_CONFLICT


def test_conflict_result_contains_existing_memory():

    candidate = make_candidate(
        "user",
        "likes",
        "coffee",
    )

    existing = make_memory(
        "user",
        "likes",
        "tea",
    )

    result = ConflictDetector().detect(
        candidate,
        existing,
    )

    assert result.existing_memory is not None
    assert result.existing_memory.id == existing.id


def test_different_subject_and_predicate_is_not_conflict():

    candidate = make_candidate(
        "user",
        "likes",
        "coffee",
    )

    existing = make_memory(
        "Anitha",
        "works_at",
        "Google",
    )

    result = ConflictDetector().detect(
        candidate,
        existing,
    )

    assert result.decision == ConflictDecision.NO_CONFLICT
from core.memory.extraction.schemas import (
    EvidenceType,
    MemoryCandidate,
    MemoryType,
)
from core.memory.relevance.models import RelevanceDecision
from core.memory.relevance.scorer import RelevanceScorer


def make_candidate(
    memory_type: MemoryType,
    content: str,
    source_text: str,
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


def test_personal_fact_is_relevant():

    candidate = make_candidate(
        MemoryType.PERSONAL_FACT,
        "User works at Microsoft",
        "I work at Microsoft.",
    )

    result = RelevanceScorer().score(candidate)

    assert result.decision == RelevanceDecision.ACCEPT
    assert result.score >= 0.75


def test_preference_is_relevant():

    candidate = make_candidate(
        MemoryType.PREFERENCE,
        "User likes tea",
        "I like tea.",
    )

    result = RelevanceScorer().score(candidate)

    assert result.decision == RelevanceDecision.ACCEPT


def test_relationship_is_relevant():

    candidate = make_candidate(
        MemoryType.RELATIONSHIP,
        "Anitha is the user's daughter",
        "My daughter Anitha lives in Chennai.",
    )

    result = RelevanceScorer().score(candidate)

    assert result.decision == RelevanceDecision.ACCEPT


def test_temporary_context_is_not_automatically_accepted():

    candidate = make_candidate(
        MemoryType.TEMPORARY_CONTEXT,
        "User is tired today",
        "I am tired today.",
    )

    result = RelevanceScorer().score(candidate)

    assert result.decision != RelevanceDecision.ACCEPT


def test_relevance_score_is_between_zero_and_one():

    candidate = make_candidate(
        MemoryType.PERSONAL_FACT,
        "User likes programming",
        "I like programming.",
    )

    result = RelevanceScorer().score(candidate)

    assert 0.0 <= result.score <= 1.0
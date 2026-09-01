from core.memory.models import Memory, MemoryStatus
from core.memory.retrieval.models import RetrievalQuery
from core.memory.retrieval.query import query_from_candidate
from core.memory.retrieval.retriever import MemoryRetriever
from core.memory.extraction.schemas import (
    EvidenceType,
    MemoryCandidate,
    MemoryType,
)


def make_memory(
    subject: str,
    predicate: str,
    value: str,
    content: str,
) -> Memory:

    return Memory(
        subject=subject,
        predicate=predicate,
        value=value,
        content=content,
        source_text=content,
    )


def test_exact_subject_and_predicate_match():

    memory = make_memory(
        "user",
        "likes",
        "tea",
        "User likes tea",
    )

    query = RetrievalQuery(
        subject="user",
        predicate="likes",
    )

    result = MemoryRetriever([memory]).retrieve(query)

    assert len(result.matches) == 1
    assert result.matches[0].memory.id == memory.id
    assert result.matches[0].score == 0.8


def test_different_predicate_is_not_returned():

    memory = make_memory(
        "user",
        "works_at",
        "Google",
        "User works at Google",
    )

    query = RetrievalQuery(
        subject="user",
        predicate="likes",
    )

    result = MemoryRetriever([memory]).retrieve(query)

    assert len(result.matches) == 1
    assert result.matches[0].score == 0.4


def test_different_subject_is_not_returned():

    memory = make_memory(
        "Anitha",
        "likes",
        "tea",
        "Anitha likes tea",
    )

    query = RetrievalQuery(
        subject="user",
        predicate="likes",
    )

    result = MemoryRetriever([memory]).retrieve(query)

    assert len(result.matches) == 1
    assert result.matches[0].score == 0.4


def test_exact_value_increases_score():

    memory = make_memory(
        "user",
        "likes",
        "tea",
        "User likes tea",
    )

    query = RetrievalQuery(
        subject="user",
        predicate="likes",
        value="tea",
    )

    result = MemoryRetriever([memory]).retrieve(query)

    assert len(result.matches) == 1
    assert result.matches[0].score == 0.9


def test_unrelated_memory_is_not_returned():

    memory = make_memory(
        "user",
        "works_at",
        "Google",
        "User works at Google",
    )

    query = RetrievalQuery(
        subject="Anitha",
        predicate="likes",
    )

    result = MemoryRetriever([memory]).retrieve(query)

    assert len(result.matches) == 0


def test_retrieval_returns_highest_score_first():

    memory1 = make_memory(
        "user",
        "likes",
        "tea",
        "User likes tea",
    )

    memory2 = make_memory(
        "user",
        "likes",
        "coffee",
        "User likes coffee",
    )

    query = RetrievalQuery(
        subject="user",
        predicate="likes",
        value="tea",
    )

    result = MemoryRetriever(
        [memory2, memory1]
    ).retrieve(query)

    assert len(result.matches) == 2
    assert result.matches[0].memory.id == memory1.id
    assert result.matches[0].score > result.matches[1].score


def test_superseded_memory_is_not_retrieved():

    memory = make_memory(
        "user",
        "likes",
        "tea",
        "User likes tea",
    )

    memory.status = MemoryStatus.SUPERSEDED

    query = RetrievalQuery(
        subject="user",
        predicate="likes",
    )

    result = MemoryRetriever([memory]).retrieve(query)

    assert len(result.matches) == 0


def test_candidate_can_be_converted_to_query():

    candidate = MemoryCandidate(
        type=MemoryType.PREFERENCE,
        subject="user",
        predicate="likes",
        value="coffee",
        content="User likes coffee",
        evidence_type=EvidenceType.EXPLICIT_USER_STATEMENT,
        source_text="I like coffee.",
    )

    query = query_from_candidate(candidate)

    assert query.subject == "user"
    assert query.predicate == "likes"
    assert query.value == "coffee"
    assert query.content == "User likes coffee"
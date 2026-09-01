from core.memory.conflict.detector import ConflictDetector
from core.memory.extraction.schemas import (
    EvidenceType,
    MemoryCandidate,
    MemoryType,
)
from core.memory.manager.manager import MemoryManager
from core.memory.relevance.scorer import RelevanceScorer
from core.memory.retrieval.retriever import MemoryRetriever
from core.memory.storage.repository import MemoryRepository
from core.memory.validation.validator import MemoryValidator


def make_candidate(value: str) -> MemoryCandidate:
    return MemoryCandidate(
        type=MemoryType.PREFERENCE,
        subject="user",
        predicate="likes",
        value=value,
        content=f"User likes {value}",
        evidence_type=EvidenceType.EXPLICIT_USER_STATEMENT,
        source_text=f"I like {value}.",
    )


class FakeExtractor:
    def extract(self, user_message: str):
        return None


def make_manager():
    repository = MemoryRepository()

    retriever = MemoryRetriever()

    return MemoryManager(
        extractor=FakeExtractor(),
        relevance_scorer=RelevanceScorer(),
        validator=MemoryValidator(),
        repository=repository,
        retriever=retriever,
        conflict_detector=ConflictDetector(),
    )


def test_valid_candidate_is_stored():

    manager = make_manager()

    result = manager.process_candidate(
        make_candidate("tea")
    )

    assert result == "STORED"

    memories = manager.repository.list_active()

    assert len(memories) == 1
    assert memories[0].value == "tea"


def test_rejected_candidate_is_not_stored():

    manager = make_manager()

    candidate = make_candidate("tea")
    candidate.source_text = "Maybe I like tea."

    result = manager.process_candidate(candidate)

    assert result == "REVIEW"
    assert manager.repository.list_all() == []


def test_conflicting_memory_is_superseded():

    manager = make_manager()

    first = make_candidate("tea")

    assert manager.process_candidate(first) == "STORED"

    second = make_candidate("coffee")

    result = manager.process_candidate(second)

    assert result == "SUPERSEDED_AND_STORED"

    memories = manager.repository.list_all()

    assert len(memories) == 2

    active = manager.repository.list_active()

    assert len(active) == 1
    assert active[0].value == "coffee"


def test_same_memory_does_not_create_conflict():

    manager = make_manager()

    first = make_candidate("tea")
    second = make_candidate("tea")

    assert manager.process_candidate(first) == "STORED"

    result = manager.process_candidate(second)

    assert result == "STORED"

    active = manager.repository.list_active()

    assert len(active) == 2

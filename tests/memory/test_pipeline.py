from core.memory.conflict.detector import ConflictDetector
from core.memory.extraction.extractor import MemoryExtractor
from core.memory.extraction.schemas import (
    EvidenceType,
    ExtractionResult,
    MemoryCandidate,
    MemoryType,
)
from core.memory.manager.manager import MemoryManager
from core.memory.relevance.scorer import RelevanceScorer
from core.memory.retrieval.retriever import MemoryRetriever
from core.memory.storage.repository import MemoryRepository
from core.memory.validation.validator import MemoryValidator


class FakeAIProvider:
    def generate_structured(
        self,
        system_prompt: str,
        user_message: str,
    ) -> ExtractionResult:

        return ExtractionResult(
            candidates=[
                MemoryCandidate(
                    type=MemoryType.PREFERENCE,
                    subject="user",
                    predicate="likes",
                    value="coffee",
                    content="User likes coffee.",
                    evidence_type=EvidenceType.EXPLICIT_USER_STATEMENT,
                    source_text=user_message,
                )
            ]
        )


def create_manager() -> MemoryManager:

    repository = MemoryRepository()
    retriever = MemoryRetriever()

    extractor = MemoryExtractor(
        ai_provider=FakeAIProvider()
    )

    return MemoryManager(
        extractor=extractor,
        relevance_scorer=RelevanceScorer(),
        validator=MemoryValidator(),
        repository=repository,
        retriever=retriever,
        conflict_detector=ConflictDetector(),
    )


def test_full_memory_pipeline_stores_extracted_memory():

    manager = create_manager()

    results = manager.process_message(
        "I love coffee."
    )

    assert results == ["STORED"]

    memories = manager.repository.list_active()

    assert len(memories) == 1
    assert memories[0].subject == "user"
    assert memories[0].predicate == "likes"
    assert memories[0].value == "coffee"


def test_empty_message_creates_no_memory():

    manager = create_manager()

    results = manager.process_message("")

    assert results == []
    assert manager.repository.list_all() == []
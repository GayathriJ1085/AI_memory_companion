from core.memory.extraction.extractor import MemoryExtractor
from core.memory.extraction.schemas import (
    EvidenceType,
    ExtractionResult,
    MemoryCandidate,
    MemoryType,
)


class MockAIProvider:

    def __init__(self, response: ExtractionResult):
        self.response = response
        self.last_system_prompt = None
        self.last_user_message = None

    def generate_structured(
        self,
        system_prompt: str,
        user_message: str,
    ) -> ExtractionResult:

        self.last_system_prompt = system_prompt
        self.last_user_message = user_message

        return self.response


def test_memory_candidate_creation():

    candidate = MemoryCandidate(
        type=MemoryType.RELATIONSHIP,
        subject="Anitha",
        predicate="daughter_of",
        value="user",
        content="Anitha is the user's daughter",
        evidence_type=EvidenceType.EXPLICIT_USER_STATEMENT,
        source_text="My daughter Anitha lives in Chennai.",
    )

    assert candidate.type == MemoryType.RELATIONSHIP
    assert candidate.subject == "Anitha"
    assert candidate.predicate == "daughter_of"
    assert candidate.value == "user"


def test_extraction_result():

    result = ExtractionResult(
        candidates=[
            MemoryCandidate(
                type=MemoryType.PREFERENCE,
                subject="user",
                predicate="likes",
                value="tea",
                content="User likes tea",
                evidence_type=EvidenceType.EXPLICIT_USER_STATEMENT,
                source_text="I like tea.",
            )
        ]
    )

    assert len(result.candidates) == 1
    assert result.candidates[0].value == "tea"


def test_memory_extractor_calls_ai_provider():

    expected_result = ExtractionResult(
        candidates=[
            MemoryCandidate(
                type=MemoryType.PREFERENCE,
                subject="user",
                predicate="likes",
                value="tea",
                content="User likes tea",
                evidence_type=EvidenceType.EXPLICIT_USER_STATEMENT,
                source_text="I like tea.",
            )
        ]
    )

    provider = MockAIProvider(expected_result)

    extractor = MemoryExtractor(provider)

    result = extractor.extract("I like tea.")

    assert len(result.candidates) == 1
    assert result.candidates[0].value == "tea"

    assert provider.last_user_message == "I like tea."


def test_empty_message_returns_no_candidates():

    expected_result = ExtractionResult(candidates=[])

    provider = MockAIProvider(expected_result)

    extractor = MemoryExtractor(provider)

    result = extractor.extract("")

    assert result.candidates == []

    # AI should not be called for an empty message.
    assert provider.last_user_message is None


def test_whitespace_message_returns_no_candidates():

    expected_result = ExtractionResult(candidates=[])

    provider = MockAIProvider(expected_result)

    extractor = MemoryExtractor(provider)

    result = extractor.extract("     ")

    assert result.candidates == []

    assert provider.last_user_message is None
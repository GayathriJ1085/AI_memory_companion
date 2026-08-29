from typing import Protocol

from core.memory.extraction.prompts import MEMORY_EXTRACTION_SYSTEM_PROMPT
from core.memory.extraction.schemas import ExtractionResult


class AIProvider(Protocol):
    """
    Interface that any AI provider must implement.

    The memory system does not care whether the underlying
    model is OpenAI, Gemini, Claude, a local model, etc.
    """

    def generate_structured(
        self,
        system_prompt: str,
        user_message: str,
    ) -> ExtractionResult:
        ...


class MemoryExtractor:
    """
    Extracts possible memory candidates from a user message.

    IMPORTANT:
    This class does NOT:
    - validate memories
    - calculate confidence
    - search existing memories
    - resolve conflicts
    - save to the database

    It only performs extraction.
    """

    def __init__(self, ai_provider: AIProvider):
        self.ai_provider = ai_provider

    def extract(self, user_message: str) -> ExtractionResult:
        """
        Extract possible memory candidates from a user message.
        """

        # Empty or whitespace-only messages contain nothing to extract.
        if not user_message or not user_message.strip():
            return ExtractionResult(candidates=[])

        result = self.ai_provider.generate_structured(
            system_prompt=MEMORY_EXTRACTION_SYSTEM_PROMPT,
            user_message=user_message.strip(),
        )

        return result
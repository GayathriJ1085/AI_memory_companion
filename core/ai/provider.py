from abc import ABC, abstractmethod

from core.ai.models import LLMResponse, Message


class AIProvider(ABC):
    """Abstract interface for an AI/LLM provider."""

    @abstractmethod
    async def generate(
        self,
        messages: list[Message],
    ) -> LLMResponse:
        """Generate a response from the AI provider."""
        raise NotImplementedError
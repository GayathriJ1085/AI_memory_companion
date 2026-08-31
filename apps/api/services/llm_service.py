import asyncio
import os

from dotenv import load_dotenv
from google import genai

from core.ai.errors import AIConfigurationError, AIProviderError
from core.ai.models import LLMResponse, Message
from core.ai.provider import AIProvider


load_dotenv()


class GeminiProvider(AIProvider):
    """Gemini implementation of the AI provider."""

    MAX_RETRIES = 3
    INITIAL_RETRY_DELAY = 2

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        model = os.getenv("GEMINI_MODEL")

        if not api_key:
            raise AIConfigurationError(
                "GEMINI_API_KEY is not configured."
            )

        if not model:
            raise AIConfigurationError(
                "GEMINI_MODEL is not configured."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def generate(
        self,
        messages: list[Message],
    ) -> LLMResponse:

        system_instruction = None
        conversation_messages = []

        for message in messages:
            if message.role == "system":
                system_instruction = message.content
            else:
                conversation_messages.append(
                    {
                        "role": (
                            "user"
                            if message.role == "user"
                            else "model"
                        ),
                        "parts": [
                            {
                                "text": message.content
                            }
                        ],
                    }
                )

        last_exception = None

        for attempt in range(self.MAX_RETRIES + 1):
            try:
                response = await self.client.aio.models.generate_content(
                    model=self.model,
                    contents=conversation_messages,
                    config={
                        "system_instruction": system_instruction,
                    }
                    if system_instruction
                    else None,
                )

                if not response.text:
                    raise AIProviderError(
                        "Gemini returned an empty response."
                    )

                return LLMResponse(
                    content=response.text,
                    model=self.model,
                )

            except AIProviderError:
                raise

            except Exception as exc:
                last_exception = exc

                error_text = str(exc).lower()

                is_temporary_error = (
                    "503" in error_text
                    or "unavailable" in error_text
                    or "high demand" in error_text
                    or "429" in error_text
                    or "resource exhausted" in error_text
                )

                if not is_temporary_error:
                    raise AIProviderError(
                        f"Gemini request failed: {exc}"
                    ) from exc

                if attempt >= self.MAX_RETRIES:
                    break

                delay = self.INITIAL_RETRY_DELAY * (2 ** attempt)

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {delay} seconds "
                    f"(attempt {attempt + 1}/{self.MAX_RETRIES})..."
                )

                await asyncio.sleep(delay)

        raise AIProviderError(
            "Gemini is temporarily unavailable after "
            f"{self.MAX_RETRIES} retries. Please try again."
        ) from last_exception


class LLMService:
    """Application service for interacting with the AI provider."""

    def __init__(self, provider: AIProvider):
        self.provider = provider

    async def generate_response(
        self,
        messages: list[Message],
    ) -> LLMResponse:
        return await self.provider.generate(messages)
import asyncio
import os

from dotenv import load_dotenv
from google import genai

from core.ai.errors import AIConfigurationError, AIProviderError
from core.ai.models import LLMResponse, Message
from core.ai.provider import AIProvider
from core.memory.extraction.schemas import ExtractionResult
from core.memory.extraction.prompts import (
    MEMORY_EXTRACTION_SYSTEM_PROMPT,
)


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
        """
        Generate a normal conversational response.
        """

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

                # --------------------------------------------------
                # 429 = quota/rate limit
                # --------------------------------------------------
                #
                # Do NOT retry blindly when the daily quota is
                # exhausted. The API response itself tells us that
                # the quota has been exceeded.
                #
                if (
                    "429" in error_text
                    or "resource_exhausted" in error_text
                    or "quota exceeded" in error_text
                ):
                    raise AIProviderError(
                        "Gemini API quota has been exhausted. "
                        "Please wait for the quota to reset or "
                        "use a different Gemini API project/model."
                    ) from exc

                # --------------------------------------------------
                # Temporary server-side failures
                # --------------------------------------------------

                is_temporary_error = (
                    "503" in error_text
                    or "unavailable" in error_text
                    or "high demand" in error_text
                )

                if not is_temporary_error:
                    raise AIProviderError(
                        f"Gemini request failed: {exc}"
                    ) from exc

                if attempt >= self.MAX_RETRIES:
                    break

                delay = self.INITIAL_RETRY_DELAY * (2 ** attempt)

                print(
                    "Gemini temporarily unavailable. "
                    f"Retrying in {delay} seconds "
                    f"(attempt {attempt + 1}/{self.MAX_RETRIES})..."
                )

                await asyncio.sleep(delay)

        raise AIProviderError(
            "Gemini is temporarily unavailable after "
            f"{self.MAX_RETRIES} retries. Please try again."
        ) from last_exception

    def generate_structured(
        self,
        system_prompt: str,
        user_message: str,
    ) -> ExtractionResult:
        """
        Generate structured memory candidates from a user message.

        Gemini returns JSON matching ExtractionResult.
        Pydantic validates the returned structure.
        """

        prompt = (
            f"{system_prompt}\n\n"
            "USER MESSAGE:\n"
            f"{user_message}"
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": ExtractionResult,
                },
            )

            if not response.text:
                raise AIProviderError(
                    "Gemini returned an empty structured response."
                )

            return ExtractionResult.model_validate_json(
                response.text
            )

        except AIProviderError:
            raise

        except Exception as exc:
            error_text = str(exc).lower()

            if (
                "429" in error_text
                or "resource_exhausted" in error_text
                or "quota exceeded" in error_text
            ):
                raise AIProviderError(
                    "Gemini API quota has been exhausted. "
                    "Memory extraction cannot run until the "
                    "quota resets or a different API project/model "
                    "is configured."
                ) from exc

            raise AIProviderError(
                f"Gemini structured extraction failed: {exc}"
            ) from exc


class LLMService:
    """Application service for interacting with the AI provider."""

    def __init__(self, provider: AIProvider):
        self.provider = provider

    async def generate_response(
        self,
        messages: list[Message],
    ) -> LLMResponse:
        return await self.provider.generate(messages)
import os

from dotenv import load_dotenv
from google import genai

from core.ai.errors import AIConfigurationError, AIProviderError
from core.ai.models import LLMResponse, Message
from core.ai.provider import AIProvider

load_dotenv()


class GeminiProvider(AIProvider):
    """Gemini implementation of the AI provider."""

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
        try:
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
            raise AIProviderError(
                f"Gemini request failed: {exc}"
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
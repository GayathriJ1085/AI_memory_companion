from core.ai.models import Message
from core.conversation.context import ConversationContext
from core.conversation.prompts import get_system_prompt
from core.conversation.session import ConversationSession


class ConversationOrchestrator:
    """
    Coordinates the Phase 1 conversation flow.

    Responsibilities:
    - Manage the current conversation session
    - Add user messages
    - Build conversation context
    - Add the companion system prompt
    - Send the conversation to the LLM service
    - Store the assistant response

    Long-term memory is intentionally not handled here.
    """

    def __init__(self, llm_service):
        self.llm_service = llm_service

    async def process_message(
        self,
        session: ConversationSession,
        user_message: str,
    ) -> str:
        """Process a user message and return the AI response."""

        if not user_message or not user_message.strip():
            raise ValueError("User message cannot be empty.")

        session.add_user_message(user_message)

        context = ConversationContext(session)

        system_prompt = get_system_prompt()

        messages = [
            Message(
                role="system",
                content=system_prompt,
            ),
            *context.get_messages(),
        ]

        llm_response = await self.llm_service.generate_response(
            messages=messages
        )

        if not llm_response or not llm_response.content.strip():
            raise RuntimeError("The AI returned an empty response.")

        session.add_assistant_message(llm_response.content)

        return llm_response.content
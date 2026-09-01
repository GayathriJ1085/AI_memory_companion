from core.ai.models import LLMResponse
from core.conversation.orchestrator import ConversationOrchestrator
from core.conversation.session import ConversationSession
from core.memory.manager.manager import MemoryManager


class ConversationService:
    """Application service for managing conversations and memories."""

    def __init__(
        self,
        orchestrator: ConversationOrchestrator,
        memory_manager: MemoryManager,
    ):
        self.orchestrator = orchestrator
        self.memory_manager = memory_manager
        self.sessions: dict[str, ConversationSession] = {}

    def get_or_create_session(
        self,
        session_id: str,
    ) -> ConversationSession:
        """Return an existing session or create a new one."""

        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationSession(session_id)

        return self.sessions[session_id]

    async def process_message(
        self,
        session_id: str,
        message: str,
    ) -> LLMResponse:
        """
        Process a user message.

        The message is:
        1. Sent through the normal conversation pipeline.
        2. Passed through the memory pipeline.
        """

        session = self.get_or_create_session(session_id)

        response_content = await self.orchestrator.process_message(
            session=session,
            user_message=message,
        )

        # Process possible long-term memories from the
        # user's original message.
        self.memory_manager.process_message(message)

        return LLMResponse(
            content=response_content,
            model=self.orchestrator.llm_service.provider.model,
        )
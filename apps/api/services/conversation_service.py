from core.ai.models import LLMResponse
from core.conversation.orchestrator import ConversationOrchestrator
from core.conversation.session import ConversationSession


class ConversationService:
    """Application service for managing Phase 1 conversations."""

    def __init__(self, orchestrator: ConversationOrchestrator):
        self.orchestrator = orchestrator
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
        """Process a message inside the requested session."""

        session = self.get_or_create_session(session_id)

        response_content = await self.orchestrator.process_message(
            session=session,
            user_message=message,
        )

        return LLMResponse(
            content=response_content,
            model=self.orchestrator.llm_service.provider.model,
        )
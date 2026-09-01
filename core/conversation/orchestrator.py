from core.ai.models import Message
from core.conversation.context import ConversationContext
from core.conversation.prompts import get_system_prompt
from core.conversation.session import ConversationSession
from core.memory.retrieval.models import RetrievalQuery
from core.memory.retrieval.retriever import MemoryRetriever


class ConversationOrchestrator:
    """
    Coordinates the conversation flow.

    Responsibilities:
    - Manage the current conversation session
    - Add user messages
    - Retrieve relevant long-term memories
    - Build conversation context
    - Add the companion system prompt
    - Send the conversation to the LLM service
    - Store the assistant response

    Long-term memory retrieval is handled here,
    while memory extraction and storage remain
    inside MemoryManager.
    """

    def __init__(
        self,
        llm_service,
        memory_retriever: MemoryRetriever | None = None,
    ):
        self.llm_service = llm_service
        self.memory_retriever = memory_retriever

    async def process_message(
        self,
        session: ConversationSession,
        user_message: str,
    ) -> str:
        """Process a user message and return the AI response."""

        if not user_message or not user_message.strip():
            raise ValueError("User message cannot be empty.")

        # --------------------------------------------------
        # 1. Add user message to current session
        # --------------------------------------------------

        session.add_user_message(user_message)

        # --------------------------------------------------
        # 2. Retrieve relevant long-term memories
        # --------------------------------------------------

        memories = []

        if self.memory_retriever is not None:

            query = RetrievalQuery(
                content=user_message,
            )

            retrieval_result = self.memory_retriever.retrieve(
                query
            )

            memories = [
                retrieved.memory
                for retrieved in retrieval_result.matches
            ]

        # --------------------------------------------------
        # 3. Build conversation context
        # --------------------------------------------------

        context = ConversationContext(
            session=session,
            memories=memories,
        )

        # --------------------------------------------------
        # 4. Build messages for the LLM
        # --------------------------------------------------

        system_prompt = get_system_prompt()

        messages = [
            Message(
                role="system",
                content=system_prompt,
            ),
            *context.get_messages(),
        ]

        # --------------------------------------------------
        # 5. Generate AI response
        # --------------------------------------------------

        llm_response = await self.llm_service.generate_response(
            messages=messages
        )

        if not llm_response or not llm_response.content.strip():
            raise RuntimeError(
                "The AI returned an empty response."
            )

        # --------------------------------------------------
        # 6. Store assistant response in session
        # --------------------------------------------------

        session.add_assistant_message(
            llm_response.content
        )

        return llm_response.content
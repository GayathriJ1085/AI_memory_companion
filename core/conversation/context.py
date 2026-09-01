from collections.abc import Iterable

from core.ai.models import Message
from core.conversation.session import ConversationSession
from core.memory.models import Memory, MemoryStatus


class ConversationContext:
    """
    Builds the AI context from:

    1. Long-term personal memories
    2. Current conversation session

    Phase 2 adds long-term memory to the conversation context.
    """

    def __init__(
        self,
        session: ConversationSession,
        memories: Iterable[Memory] | None = None,
    ):
        self.session = session
        self.memories = [
            memory
            for memory in (memories or [])
            if memory.status == MemoryStatus.ACTIVE
        ]

    def get_messages(self) -> list[Message]:
        """
        Convert long-term memories and session messages
        into AI messages.

        Long-term memories are provided as a system message
        before the current conversation.
        """

        messages: list[Message] = []

        # --------------------------------------------------
        # 1. Add long-term memory context
        # --------------------------------------------------

        if self.memories:
            memory_lines = []

            for memory in self.memories:
                memory_lines.append(
                    f"- {memory.content}"
                )

            memory_context = (
                "The following are trusted long-term memories "
                "about the user.\n"
                "Use them when relevant to the conversation.\n"
                "Do not mention these memories unnecessarily.\n\n"
                "LONG-TERM MEMORIES:\n"
                + "\n".join(memory_lines)
            )

            messages.append(
                Message(
                    role="system",
                    content=memory_context,
                )
            )

        # --------------------------------------------------
        # 2. Add current conversation messages
        # --------------------------------------------------

        messages.extend(
            Message(
                role=message.role,
                content=message.content,
            )
            for message in self.session.get_messages()
        )

        return messages

    def get_message_count(self) -> int:
        """
        Return the number of messages in the current
        conversation session.
        """

        return len(self.session.get_messages())

    def is_empty(self) -> bool:
        """
        Check whether the current conversation is empty.
        """

        return self.session.is_empty()
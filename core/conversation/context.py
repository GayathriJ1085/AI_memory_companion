from core.ai.models import Message
from core.conversation.session import ConversationSession


class ConversationContext:
    """
    Builds the AI context from the current conversation session.

    Phase 1 only uses the current session.
    Long-term memory will be added in Phase 2.
    """

    def __init__(self, session: ConversationSession):
        self.session = session

    def get_messages(self) -> list[Message]:
        """Convert session messages into AI messages."""

        return [
            Message(
                role=message.role,
                content=message.content,
            )
            for message in self.session.get_messages()
        ]

    def get_message_count(self) -> int:
        """Return the number of messages in the current context."""

        return len(self.session.get_messages())

    def is_empty(self) -> bool:
        """Check whether the context contains any messages."""

        return self.session.is_empty()
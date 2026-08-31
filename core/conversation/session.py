from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal


Role = Literal["user", "assistant"]


@dataclass
class ConversationMessage:
    """A single message in the current conversation session."""

    role: Role
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


class ConversationSession:
    """
    Stores temporary conversation history for one active session.

    This is NOT long-term memory.
    Session data exists only while the application keeps the session object.
    """

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: list[ConversationMessage] = []
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def add_user_message(self, content: str) -> None:
        """Add a user message to the current session."""

        self._add_message("user", content)

    def add_assistant_message(self, content: str) -> None:
        """Add an AI assistant response to the current session."""

        self._add_message("assistant", content)

    def _add_message(self, role: Role, content: str) -> None:
        """Internal method for adding a validated message."""

        if not content or not content.strip():
            raise ValueError("Message content cannot be empty.")

        message = ConversationMessage(
            role=role,
            content=content.strip(),
        )

        self.messages.append(message)
        self.updated_at = message.timestamp

    def get_messages(self) -> list[ConversationMessage]:
        """Return a copy of the current conversation history."""

        return self.messages.copy()

    def get_message_count(self) -> int:
        """Return the number of messages in the session."""

        return len(self.messages)

    def clear(self) -> None:
        """Clear the current session history."""

        self.messages.clear()
        self.updated_at = datetime.utcnow()

    def is_empty(self) -> bool:
        """Check whether the session contains any messages."""

        return len(self.messages) == 0
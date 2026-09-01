from core.ai.models import Message
from core.conversation.context import ConversationContext
from core.conversation.session import ConversationSession
from core.memory.models import Memory, MemoryStatus


def create_memory(
    subject: str,
    predicate: str,
    value: str,
    content: str,
) -> Memory:
    return Memory(
        subject=subject,
        predicate=predicate,
        value=value,
        content=content,
        source_text=content,
        status=MemoryStatus.ACTIVE,
    )


def test_conversation_context_contains_current_session_messages():

    session = ConversationSession("test-session")

    session.add_user_message("Hello")
    session.add_assistant_message("Hi! How are you?")

    context = ConversationContext(session)

    messages = context.get_messages()

    assert len(messages) == 2

    assert messages[0].role == "user"
    assert messages[0].content == "Hello"

    assert messages[1].role == "assistant"
    assert messages[1].content == "Hi! How are you?"


def test_conversation_context_can_include_long_term_memories():

    session = ConversationSession("test-session")

    session.add_user_message(
        "What do you remember about me?"
    )

    memories = [
        create_memory(
            subject="user",
            predicate="likes",
            value="tea",
            content="User likes tea.",
        ),
        create_memory(
            subject="user",
            predicate="goes_for_walk",
            value="6 PM",
            content="User usually goes for a walk at 6 PM.",
        ),
    ]

    context = ConversationContext(
        session=session,
        memories=memories,
    )

    messages = context.get_messages()

    assert len(messages) == 2

    assert messages[0].role == "system"

    assert "tea" in messages[0].content
    assert "6 PM" in messages[0].content

    assert messages[1].role == "user"
    assert messages[1].content == "What do you remember about me?"


def test_conversation_context_without_memories_still_works():

    session = ConversationSession("test-session")

    session.add_user_message("Hello")

    context = ConversationContext(
        session=session,
        memories=[],
    )

    messages = context.get_messages()

    assert len(messages) == 1

    assert messages[0].role == "user"
    assert messages[0].content == "Hello"


def test_superseded_memories_are_not_added_to_context():

    session = ConversationSession("test-session")

    session.add_user_message(
        "What do I like?"
    )

    active_memory = create_memory(
        subject="user",
        predicate="likes",
        value="coffee",
        content="User likes coffee.",
    )

    superseded_memory = create_memory(
        subject="user",
        predicate="likes",
        value="tea",
        content="User likes tea.",
    )

    superseded_memory.status = MemoryStatus.SUPERSEDED

    context = ConversationContext(
        session=session,
        memories=[
            active_memory,
            superseded_memory,
        ],
    )

    messages = context.get_messages()

    memory_context = messages[0].content

    assert "coffee" in memory_context
    assert "tea" not in memory_context
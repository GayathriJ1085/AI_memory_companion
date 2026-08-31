import asyncio

from core.ai.models import LLMResponse
from core.conversation.orchestrator import ConversationOrchestrator
from core.conversation.session import ConversationSession


class MockLLMService:
    """Mock LLM service used to test the conversation orchestrator."""

    def __init__(self):
        self.calls = []

    async def generate_response(self, messages):
        self.calls.append(messages)

        return LLMResponse(
            content="Hello! This is a mock AI response.",
            model="mock-model",
        )


async def main():
    print("=" * 60)
    print("ORCHESTRATOR MOCK TEST")
    print("=" * 60)

    mock_llm = MockLLMService()
    orchestrator = ConversationOrchestrator(mock_llm)

    session = ConversationSession("test-session-001")

    # ---------------------------------------------------------
    # FIRST MESSAGE
    # ---------------------------------------------------------

    response = await orchestrator.process_message(
        session,
        "Hello!",
    )

    print("\nUser:")
    print("Hello!")

    print("\nAI:")
    print(response)

    # ---------------------------------------------------------
    # SECOND MESSAGE
    # ---------------------------------------------------------

    response = await orchestrator.process_message(
        session,
        "How are you?",
    )

    print("\nUser:")
    print("How are you?")

    print("\nAI:")
    print(response)

    # ---------------------------------------------------------
    # SESSION HISTORY
    # ---------------------------------------------------------

    messages = session.get_messages()

    print("\n" + "-" * 60)
    print("SESSION HISTORY")
    print("-" * 60)

    for message in messages:
        print(f"{message.role.upper()}: {message.content}")

    # ---------------------------------------------------------
    # LLM CALLS
    # ---------------------------------------------------------

    print("\n" + "-" * 60)
    print("LLM CALLS")
    print("-" * 60)

    print(f"Number of LLM calls: {len(mock_llm.calls)}")

    # ---------------------------------------------------------
    # ASSERTIONS
    # ---------------------------------------------------------

    # Two user requests = two LLM calls
    assert len(mock_llm.calls) == 2

    # Two user messages + two assistant responses
    assert len(messages) == 4

    # First user message
    assert messages[0].role == "user"
    assert messages[0].content == "Hello!"

    # First assistant response
    assert messages[1].role == "assistant"
    assert messages[1].content == "Hello! This is a mock AI response."

    # Second user message
    assert messages[2].role == "user"
    assert messages[2].content == "How are you?"

    # Second assistant response
    assert messages[3].role == "assistant"
    assert messages[3].content == "Hello! This is a mock AI response."

    # ---------------------------------------------------------
    # VERIFY CONTEXT SENT TO LLM
    # ---------------------------------------------------------

    # First call:
    # system prompt + first user message
    assert len(mock_llm.calls[0]) == 2

    assert mock_llm.calls[0][0].role == "system"
    assert mock_llm.calls[0][0].content.strip()

    assert mock_llm.calls[0][1].role == "user"
    assert mock_llm.calls[0][1].content == "Hello!"

    # Second call:
    # system prompt
    # first user
    # first assistant
    # second user
    assert len(mock_llm.calls[1]) == 4

    assert mock_llm.calls[1][0].role == "system"
    assert mock_llm.calls[1][1].role == "user"
    assert mock_llm.calls[1][2].role == "assistant"
    assert mock_llm.calls[1][3].role == "user"

    assert mock_llm.calls[1][3].content == "How are you?"

    print("\n" + "=" * 60)
    print("ALL ORCHESTRATOR TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
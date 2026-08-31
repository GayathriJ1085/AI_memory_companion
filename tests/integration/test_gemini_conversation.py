import asyncio

from core.conversation.orchestrator import ConversationOrchestrator
from core.conversation.session import ConversationSession
from apps.api.services.llm_service import GeminiProvider, LLMService


async def main():
    print("=" * 60)
    print("GEMINI CONVERSATION INTEGRATION TEST")
    print("=" * 60)

    # Create the real Gemini provider
    provider = GeminiProvider()

    # Create the application-level LLM service
    llm_service = LLMService(provider)

    # Create the conversation orchestrator
    orchestrator = ConversationOrchestrator(llm_service)

    # Create a fresh session
    session = ConversationSession("gemini-test-001")

    # ---------------------------------------------------------
    # FIRST MESSAGE
    # ---------------------------------------------------------

    print("\nUser:")
    print("Hello! My name is Mohit.")

    response = await orchestrator.process_message(
        session,
        "Hello! My name is Mohit.",
    )

    print("\nAI:")
    print(response)

    # ---------------------------------------------------------
    # SECOND MESSAGE
    # ---------------------------------------------------------

    print("\nUser:")
    print("What is my name?")

    response = await orchestrator.process_message(
        session,
        "What is my name?",
    )

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
    # BASIC VALIDATION
    # ---------------------------------------------------------

    assert len(messages) == 4

    assert messages[0].role == "user"
    assert messages[1].role == "assistant"
    assert messages[2].role == "user"
    assert messages[3].role == "assistant"

    assert messages[0].content == "Hello! My name is Mohit."
    assert messages[2].content == "What is my name?"

    assert messages[1].content.strip()
    assert messages[3].content.strip()

    print("\n" + "=" * 60)
    print("GEMINI INTEGRATION TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
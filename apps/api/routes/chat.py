from fastapi import APIRouter, HTTPException

from apps.api.schemas.chat import ChatRequest, ChatResponse
from apps.api.services.conversation_service import ConversationService
from apps.api.services.llm_service import GeminiProvider, LLMService
from core.ai.errors import AIConfigurationError, AIProviderError
from core.conversation.orchestrator import ConversationOrchestrator
from core.memory.conflict.detector import ConflictDetector
from core.memory.extraction.extractor import MemoryExtractor
from core.memory.manager.manager import MemoryManager
from core.memory.relevance.scorer import RelevanceScorer
from core.memory.retrieval.retriever import MemoryRetriever
from core.memory.storage.repository import MemoryRepository
from core.memory.validation.validator import MemoryValidator


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

memory_router = APIRouter(
    prefix="/memory",
    tags=["Memory"],
)


def create_memory_manager(
    provider: GeminiProvider,
    repository: MemoryRepository,
    retriever: MemoryRetriever,
) -> MemoryManager:
    """
    Create the Phase 2 memory-processing pipeline.

    The repository and retriever are shared with the
    conversation layer so newly stored memories can
    later be retrieved during conversation.
    """

    extractor = MemoryExtractor(
        ai_provider=provider,
    )

    return MemoryManager(
        extractor=extractor,
        relevance_scorer=RelevanceScorer(),
        validator=MemoryValidator(),
        repository=repository,
        retriever=retriever,
        conflict_detector=ConflictDetector(),
    )


def create_conversation_service() -> ConversationService:
    """
    Create all application services and connect
    the conversation and memory layers.
    """

    provider = GeminiProvider()

    llm_service = LLMService(
        provider
    )

    # Shared memory infrastructure.
    repository = MemoryRepository()
    retriever = MemoryRetriever()

    # Memory processing pipeline.
    memory_manager = create_memory_manager(
        provider=provider,
        repository=repository,
        retriever=retriever,
    )

    # Conversation pipeline.
    orchestrator = ConversationOrchestrator(
        llm_service=llm_service,
        memory_retriever=retriever,
    )

    return ConversationService(
        orchestrator=orchestrator,
        memory_manager=memory_manager,
    )


conversation_service = create_conversation_service()


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(request: ChatRequest):
    try:
        response = await conversation_service.process_message(
            session_id=request.session_id,
            message=request.message,
        )

        return ChatResponse(
            session_id=request.session_id,
            response=response.content,
            model=response.model,
        )

    except AIConfigurationError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except AIProviderError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="An unexpected server error occurred.",
        ) from exc


@memory_router.get("")
async def get_memories():
    """
    Return all memories currently stored.

    Mainly useful for development and testing.
    """

    memories = (
        conversation_service
        .memory_manager
        .repository
        .list_all()
    )

    return [
        memory.model_dump(mode="json")
        for memory in memories
    ]
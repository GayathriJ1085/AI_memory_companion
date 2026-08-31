from fastapi import APIRouter, HTTPException

from apps.api.schemas.chat import ChatRequest, ChatResponse
from apps.api.services.conversation_service import ConversationService
from apps.api.services.llm_service import GeminiProvider, LLMService
from core.ai.errors import AIConfigurationError, AIProviderError
from core.conversation.orchestrator import ConversationOrchestrator


router = APIRouter(prefix="/chat", tags=["Chat"])


def create_conversation_service() -> ConversationService:
    provider = GeminiProvider()
    llm_service = LLMService(provider)
    orchestrator = ConversationOrchestrator(llm_service)

    return ConversationService(orchestrator)


conversation_service = create_conversation_service()


@router.post("", response_model=ChatResponse)
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
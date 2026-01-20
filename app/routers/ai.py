from fastapi import APIRouter, Depends

from app.api.dependencies import get_chat_service
from app.schemas.schemas import UserRequest, AnalyzeResponse
from app.services.chat_service import ChatService

router = APIRouter(tags=["agent"])


@router.post("/agent/analyze/", response_model=AnalyzeResponse)
async def analyze_message(
    request: UserRequest,
    service: ChatService = Depends(get_chat_service),
):
    """
    Endpoint to analyze a user's message.

    :param request: The user request containing the message to analyze.
    :param service: The chat service dependency.
    :return: The analysis result.
    """
    return await service.analyze_and_save(request.message)

from fastapi import APIRouter, Depends, WebSocket

from app.quiz.websocket.quiz import QuizWebsocketService
from core.helpers.websocket.permission.permissions import get_cookie_or_token


quiz_websocket_router = APIRouter()


@quiz_websocket_router.websocket("/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str = None,
    access_token: str = Depends(get_cookie_or_token),
):
    await QuizWebsocketService().handler(
        websocket,
        session_id,
        access_token,
    )

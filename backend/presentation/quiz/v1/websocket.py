from fastapi import APIRouter, Depends, WebSocket

from app.quiz.websocket.quiz import QuizWebsocketService
from app.quiz.dependencies.quiz import get_path_quiz_id
from core.helpers.websocket.permission.permissions import get_cookie_or_token
from core.versioning import version


quiz_websocket_router = APIRouter()


@quiz_websocket_router.websocket("/{quiz_id}/ws")
@version(1)
async def websocket_endpoint(
    websocket: WebSocket,
    quiz_id: str = None,
    access_token=Depends(get_cookie_or_token),
):
    print("ASDASDSADASD")
    await QuizWebsocketService().handler(websocket, quiz_id, access_token)


@quiz_websocket_router.get("/{quiz_id}/websucker")
@version(1)
async def action_docs(quiz_id: str):
    print("ASDASDSADASD")
    return "Hi!"

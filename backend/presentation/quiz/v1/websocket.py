from fastapi import APIRouter, Depends, WebSocket

from app.quiz.websocket.quiz import QuizWebsocketService
from app.quiz.dependencies.quiz import get_path_quiz_id
from core.helpers.websocket.permission.permissions import AllowAll, IsAuthenticated
from core.versioning import version


quiz_websocket_router = APIRouter()


@quiz_websocket_router.websocket("/quizCreate/{quiz_id}")
@version(1)
async def create_quiz_session(
    websocket: WebSocket,
    token: str,
    quiz_id: int = Depends(get_path_quiz_id),
):
    await QuizWebsocketService(websocket, [IsAuthenticated]).start_create_session(
        quiz_id=quiz_id,
        access_token=token,
    )


@quiz_websocket_router.websocket("/quizJoin/{quiz_id}/{session_id}")
@version(1)
async def join_quiz_session(
    websocket: WebSocket,
    session_id: str,
    username: str,
    quiz_id: int = Depends(get_path_quiz_id),
):
    await QuizWebsocketService(websocket, [AllowAll]).start_join_session(
        quiz_id=quiz_id,
        session_id=session_id,
        username=username,
    )


@quiz_websocket_router.get("/action_docs")
@version(1)
async def action_docs():
    return "WIP :)"

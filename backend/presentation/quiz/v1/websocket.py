from fastapi import APIRouter, Depends, WebSocket

from app.quiz.websocket.quiz import QuizWebSocketService
from app.quiz.websocket.docs import quiz_actions
from app.quiz.dependencies.quiz import get_path_quiz_id
from core.helpers.websocket.dependencies.docs import parse_actions
from core.helpers.websocket.permission.permissions import AllowAll, IsAuthenticated
from core.versioning import version


quiz_websocket_router = APIRouter()


@quiz_websocket_router.websocket("/quizCreate/{quiz_id}")
@version(1)
async def create_quiz_session(
    websocket: WebSocket,
    access_token: str,
    client_token: str,
    quiz_id: int = Depends(get_path_quiz_id),
):
    await QuizWebSocketService(websocket, [IsAuthenticated]).start_create_session(
        quiz_id=quiz_id,
        access_token=access_token,
        client_token=client_token,
    )


@quiz_websocket_router.websocket("/quizJoin/{session_id}")
@version(1)
async def join_quiz_session(
    websocket: WebSocket,
    session_id: int,
    username: str,
    client_token: str,
):
    await QuizWebSocketService(websocket, [AllowAll]).start_join_session(
        session_id=session_id,
        username=username,
        client_token=client_token,
    )


@quiz_websocket_router.get("/quiz/action_docs")
@version(1)
async def action_docs():
    return parse_actions(quiz_actions)

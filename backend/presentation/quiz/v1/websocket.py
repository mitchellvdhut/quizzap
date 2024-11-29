import logging
from fastapi import APIRouter, Depends, WebSocket

# from app.quiz.websocket.quiz import QuizWebsocketService
from app.quiz.dependencies.quiz import get_path_quiz_id
from app.quiz.dependencies.websocket import get_cookie_or_token
from core.versioning import version


quiz_websocket_router = APIRouter()


@quiz_websocket_router.websocket("/quizCreate/{quiz_id}")
@version(1)
async def websocket_endpoint(
    websocket: WebSocket,
    quiz_id: int = Depends(get_path_quiz_id),
    access_token: str = Depends(get_cookie_or_token),
):
    logger = logging.getLogger("root")

    logger.info("Creating new session.")
    logger.debug(f"{quiz_id = }")
    logger.debug(f"{access_token = }")

    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        logger.info(f"Received message: '{data}'")
        await websocket.send_text(f"Message text was: {data}")


@quiz_websocket_router.get("/action_docs")
@version(1)
async def action_docs():
    return "WIP :)"

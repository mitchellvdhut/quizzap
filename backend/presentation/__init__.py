"""Bundle all endpoints."""

from fastapi import APIRouter

from presentation.home.v1.home import home_v1_router
from presentation.quiz.v1.quiz import quiz_v1_router
from presentation.quiz.v1.question import question_v1_router
from presentation.quiz.v1.answer import answer_v1_router
from presentation.quiz.v1.websocket import quiz_websocket_router
from presentation.user.v1.user import user_v1_router
from presentation.auth.v1.auth import auth_v1_router
from presentation.me.v1.me import me_v1_router


question_v1_router.include_router(answer_v1_router, prefix="/{question_id}/answers", tags=["Answers"])
quiz_v1_router.include_router(question_v1_router, prefix="/{quiz_id}/questions", tags=["Questions"])

quiz_v1_router.include_router(quiz_websocket_router, prefix="/websocket")


router = APIRouter()
router.include_router(home_v1_router, prefix="", tags=["Home"])
router.include_router(auth_v1_router, prefix="/auth", tags=["Auth"])
router.include_router(user_v1_router, prefix="/users", tags=["Users"])
router.include_router(me_v1_router, prefix="/me", tags=["Me"])
router.include_router(quiz_v1_router, prefix="/quizzes", tags=["Quizzes"])


__all__ = ["router"]

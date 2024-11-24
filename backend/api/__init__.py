"""Bundle all endpoints."""

from fastapi import APIRouter

from api.home.v1.home import home_v1_router
from api.quiz.v1.quiz import quiz_v1_router
from api.quiz.v1.question import question_v1_router
from api.user.v1.user import user_v1_router
from api.auth.v1.auth import auth_v1_router
from api.me.v1.me import me_v1_router


quiz_v1_router.include_router(question_v1_router, prefix="/{quiz_id}/questions", tags=["Questions"])


router = APIRouter()
router.include_router(home_v1_router, prefix="", tags=["Home"])
router.include_router(auth_v1_router, prefix="/auth", tags=["Auth"])
router.include_router(user_v1_router, prefix="/users", tags=["Users"])
router.include_router(me_v1_router, prefix="/me", tags=["Me"])
router.include_router(quiz_v1_router, prefix="/quizzes", tags=["Quizzes"])


__all__ = ["router"]

from fastapi import Request
from sqlalchemy.orm import Session
from app.quiz.exceptions.quiz import QuizNotFoundException
from app.quiz.services.quiz import QuizService
from app.user.services.user import UserService
from core.exceptions.base import UnauthorizedException
from core.fastapi.dependencies.permission.permission_dependency import BasePermission
from core.helpers.hashids import decode_single


def get_hashed_param_from_path(param, request):
    hashed_id = request.path_params.get(param)
    return decode_single(hashed_id)


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request, session: Session) -> bool:
        del session

        return request.user.id is not None


class IsQuizOwner(BasePermission):
    async def has_permission(self, request: Request, session: Session) -> bool:
        quiz_id = get_hashed_param_from_path("quiz_id", request)

        try:
            QuizService(session).get_quiz(quiz_id)
        except QuizNotFoundException:
            return False


        return True


class IsUserOwner(BasePermission):
    async def has_permission(self, request: Request, session: Session) -> bool:
        del session
        
        user_id = get_hashed_param_from_path("user_id", request)

        if user_id != request.user.id:
            return False

        return True


class IsAdmin(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request, session: Session) -> bool:
        user_id = request.user.id
        if not user_id:
            return False

        return await UserService(session).is_admin(user_id=user_id)


class AllowAll(BasePermission):
    async def has_permission(self, request: Request, session: Session) -> bool:
        del request, session

        return True

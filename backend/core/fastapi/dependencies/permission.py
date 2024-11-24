from abc import ABC, abstractmethod
from typing import List, Type

from fastapi import Depends, Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from sqlalchemy.orm import Session

from app.user.services.user import UserService
from app.quiz.exceptions.quiz import QuizNotFoundException
from app.quiz.services.quiz import QuizService
from core.fastapi.dependencies.database import get_db
from core.exceptions.base import (
    CustomException,
    UnauthorizedException,
)
from core.helpers.hashids import decode_single


def get_hashed_param_from_path(param, request):
    hashed_id = request.path_params.get(param)
    return decode_single(hashed_id)


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request, session: Session) -> bool:
        ...


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


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List[List[Type[BasePermission]]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request, session: Session = Depends(get_db)):
        exceptions = {}
        for i, permission_combo in enumerate(self.permissions):
            exceptions[i] = []

            for permission in permission_combo:
                cls = permission()
                if not await cls.has_permission(request=request, session=session):

                    exceptions[i].append(cls.exception)
                    break

        if any(len(excs) == 0 for _, excs in exceptions.items()):
            return

        for _, excs in exceptions.items():
            if len(excs) > 0:
                raise excs[0]

from abc import ABC, abstractmethod
import logging
from typing import List, Type, Union
from fastapi import Depends, Request
from fastapi.security.base import SecurityBase
from fastapi.openapi.models import APIKey, APIKeyIn
from sqlalchemy.orm import Session

from app.user.services.user import UserService
from app.quiz.exceptions.quiz import QuizNotFoundException
from app.quiz.services.quiz import QuizService
from core.fastapi.dependencies.database import get_db
from core.helpers.hashids import decode_single
from core.exceptions.base import UnauthorizedException


def get_hashed_param_from_path(param, request):
    hashed_id = request.path_params.get(param)
    return decode_single(hashed_id)


class Keyword(ABC):
    pass


class AND(Keyword):
    pass


class OR(Keyword):
    pass


class NOT(Keyword):
    pass


class BasePermission(ABC):
    @abstractmethod
    async def has_permission(self, request: Request, session: Session) -> bool:
        del request


PermList = List[Union[Type[BasePermission], Type[Keyword], List]]


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
    def __init__(self, *perms: PermList) -> None:
        self.perms = perms
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request, session: Session = Depends(get_db)):
        access = await self.check_permissions(self.perms, request, session)

        if not access:
            raise UnauthorizedException

    @staticmethod
    async def check_permissions(perms: PermList, request: Request, session: Session) -> bool:
        if not perms:
            return False

        if not await PermissionDependency.is_valid_perms(perms):
            raise ValueError("Invalid perms.")
        
        invert_next = False
        skip_until_or = False
        has_permission = False

        for perm in perms:
            if isinstance(perm, list) or isinstance(perm, tuple):
                if skip_until_or:
                    continue

                has_permission = await PermissionDependency.check_permissions(perm, request, session)
                has_permission = not has_permission if invert_next else has_permission
                invert_next = False
                continue

            if issubclass(perm, Keyword):
                if perm is OR:
                    skip_until_or = False

                    if has_permission:
                        return True
                    continue

                if skip_until_or:
                    continue

                if perm is NOT:
                    invert_next = True
                    continue

                if perm is AND and not has_permission:
                    skip_until_or = True
                    continue

            if skip_until_or:
                continue

            if issubclass(perm, BasePermission):
                has_permission = await perm().has_permission(request, session)
                has_permission = not has_permission if invert_next else has_permission
                invert_next = False
                continue

        return has_permission

    @staticmethod
    async def is_valid_perms(perms: PermList) -> bool:
        for index, perm in enumerate(perms):
            if isinstance(perm, list) or isinstance(perm, tuple):
                if not await PermissionDependency.is_valid_perms(perm):
                    return False
                continue

            if issubclass(perm, BasePermission):
                if index == len(perms) - 1:
                    return True

                next_perm = perms[index + 1]
                if isinstance(next_perm, list) or issubclass(next_perm, BasePermission):
                    logging.error(f"TWO PERMISSIONS ADJACENT: {perms}")
                    return False

                if isinstance(next_perm, NOT):
                    logging.error(f"'NOT' AFTER PERMISSON: {perms}")
                    return False

                continue

            if issubclass(perm, Keyword):
                if index == len(perms) - 1:
                    logging.error(f"ENDS ON KEYWORD: {perms}")
                    return False

                if index == 0 and perm is not NOT:
                    logging.error(f"START ON 'AND' or 'OR': {perms}")
                    return False

                if perm is NOT:
                    next_perm = perms[index + 1]
                    if not isinstance(next_perm, list) and not issubclass(
                        next_perm, BasePermission
                    ):
                        logging.error(f"'NOT' LOOKS AT KEYWORD: {perms}")
                        return False

                else:
                    next_perm = perms[index + 1]
                    if next_perm is AND or next_perm is OR:
                        logging.error(f"'AND' or 'OR' LOOKS AT 'AND' or 'OR': {perms}")
                        return False
                continue

        return True


def remove_class_prefix(input_string: str) -> str:
    """Print a permission statement to be readable"""

    cleaned_string = input_string.replace("<class 'classes.", "")
    cleaned_string = cleaned_string.replace("'>", "")

    return cleaned_string

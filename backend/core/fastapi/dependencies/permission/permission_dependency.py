from abc import ABC, abstractmethod
import logging
from typing import Type, Union
from fastapi import Depends, Request
from fastapi.security.base import SecurityBase
from fastapi.openapi.models import APIKey, APIKeyIn
from sqlalchemy.orm import Session

from core.fastapi.dependencies.permission.keyword import AND, NOT, OR, Keyword
from core.fastapi.dependencies.database import get_db
from core.exceptions.base import UnauthorizedException


class BasePermission(ABC):
    @abstractmethod
    async def has_permission(self, request: Request, session: Session) -> bool:
        del request


PermItem = Union[Type[BasePermission], Type[Keyword], tuple, list]
PermList = Union[tuple[PermItem], list[PermItem]]


class PermissionDependency(SecurityBase):
    def __init__(self, *perms: PermList) -> None:
        self.perms = perms
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__
        self.base_perm_type = BasePermission

    async def __call__(self, request: Request, session: Session = Depends(get_db)):
        self.curr_request = request
        self.curr_session = session

        access = await self.check_permissions(self.perms)
        
        if not access:
            raise UnauthorizedException

    async def execute_perm(self, permission: BasePermission):
        request = self.curr_request
        session = self.curr_session

        return await permission().has_permission(request, session)

    async def check_permissions(self, perms: PermList) -> bool:
        if not perms:
            return False

        if not await self.is_valid_perms(perms):
            raise ValueError("Invalid perms.")

        invert_next = False
        skip_until_or = False
        has_permission = False

        for perm in perms:
            if isinstance(perm, list) or isinstance(perm, tuple):
                if skip_until_or:
                    continue

                has_permission = await self.check_permissions(perm)
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

            if issubclass(perm, self.base_perm_type):
                has_permission = await self.execute_perm(perm)
                has_permission = not has_permission if invert_next else has_permission
                invert_next = False
                continue

        return has_permission

    async def is_valid_perms(self, perms: PermList) -> bool:
        for index, perm in enumerate(perms):
            if isinstance(perm, list) or isinstance(perm, tuple):
                if not await self.is_valid_perms(perm):
                    return False
                continue

            if issubclass(perm, self.base_perm_type):
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

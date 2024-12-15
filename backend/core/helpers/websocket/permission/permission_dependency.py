from abc import ABC, abstractmethod
from typing import Type, Union

from core.config import config
from core.enums.internal import Modes
from core.fastapi.dependencies.permission.permission_dependency import (
    PermissionDependency,
)
from core.fastapi.dependencies.permission.keyword import Keyword
from core.exceptions.base import UnauthorizedException


class BaseWebSocketPermission(ABC):
    @abstractmethod
    async def has_permission(self, pool_id: int, access_token: str, **kwargs) -> bool:
        del pool_id, access_token, kwargs


PermItem = Union[Type[BaseWebSocketPermission], Type[Keyword], tuple, list]
PermList = Union[tuple[PermItem], list[PermItem]]


class WebSocketPermission(PermissionDependency):
    def __init__(self, *perms):
        super().__init__(*perms)
        self.base_perm_type = BaseWebSocketPermission

    async def __call__(
        self,
        access_token: str,
        **kwargs,
    ):
        if config.MODE == Modes.ANARCHY.value:
            return True
        
        self.access_token = access_token
        self.kwargs = kwargs

        access = await self.check_permissions(self.perms)

        if not access:
            raise UnauthorizedException

    async def execute_perm(self, permission: BaseWebSocketPermission):
        access_token = self.access_token
        kwargs = self.kwargs

        return await permission().has_permission(access_token, **kwargs)

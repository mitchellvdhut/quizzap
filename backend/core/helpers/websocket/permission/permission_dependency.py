from abc import ABC, abstractmethod
from typing import List, Type, Union

from core.fastapi.dependencies.permission.permission_dependency import PermissionDependency
from core.fastapi.dependencies.permission.keyword import Keyword
from core.exceptions.base import UnauthorizedException


class BaseWebsocketPermission(ABC):
    @abstractmethod
    async def has_permission(self, pool_id: int) -> bool:
        del pool_id


PermList = List[Union[Type[BaseWebsocketPermission], Type[Keyword], List]]


class WebsocketPermission(PermissionDependency):
    def __init__(self, *perms):
        super().__init__(*perms)
        self.base_perm_type = BaseWebsocketPermission

    async def __call__(self, pool_id: int):
        self.curr_pool_id = pool_id

        access = await self.check_permissions(self.perms)

        if not access:
            raise UnauthorizedException

    async def execute_perm(self, permission: BaseWebsocketPermission):
        pool_id = self.curr_pool_id

        return await permission().has_permission(pool_id)

"""
Permission class to approve and refuse access on websockets.
"""
from core.helpers.token.token_helper import TokenHelper
from core.helpers.websocket.permission.permission_dependency import BaseWebsocketPermission

from core.exceptions.base import CustomException


class AllowAll(BaseWebsocketPermission):
    async def has_permission(self, pool_id: str, access_token: str, **kwargs) -> bool:
        del pool_id, access_token, kwargs
        return True


class IsAuthenticated(BaseWebsocketPermission):
    async def has_permission(self, pool_id: str, access_token: str, **kwargs) -> bool:
        del pool_id, kwargs

        if not access_token:
            return False

        try:
            TokenHelper.decode(token=access_token)

        except CustomException:
            return False

        return True

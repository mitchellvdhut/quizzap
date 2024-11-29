"""
Permission class to approve and refuse access on websockets.
"""
from core.helpers.token.token_helper import TokenHelper
from core.helpers.websocket.permission.permission_dependency import BaseWebsocketPermission

from core.exceptions.base import CustomException


class AllowAll(BaseWebsocketPermission):
    async def has_permission(self, **kwargs) -> bool:
        return True


class IsAuthenticated(BaseWebsocketPermission):
    async def has_permission(self, **kwargs) -> bool:
        access_token = kwargs.get("access_token")

        if not access_token:
            return False

        try:
            TokenHelper.decode(token=access_token)

        except CustomException:
            return False

        return True

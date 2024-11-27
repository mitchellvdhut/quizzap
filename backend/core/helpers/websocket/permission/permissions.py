"""
Permission class to approve and refuse access on websockets.
"""


from typing import Annotated
from fastapi import Cookie, Query, WebSocketException, status
from core.helpers.token.token_helper import TokenHelper
from core.helpers.websocket.permission.permission_dependency import BaseWebsocketPermission

from core.exceptions.base import CustomException

# pylint: disable=too-few-public-methods


async def get_cookie_or_token(
    access_token: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    """Retrieve access_token from cookie or query parameter"""
    if access_token is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return access_token or token


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

"""Module containing the base websocket service for other variations to extend upon.
"""

from fastapi import WebSocket
from core.helpers.websocket import manager
from core.db.enums import WebsocketActionEnum
from core.helpers.websocket.schemas.packet import QuizWebsocketPacketSchema
from core.helpers.websocket.base import BaseWebsocketService
from core.helpers.websocket.permission.permission_dependency import PermList


class QuizWebsocketService(BaseWebsocketService):
    def __init__(self, perms: PermList | None = None):
        actions = {
            WebsocketActionEnum.POOL_MESSAGE.value: self.handle_pool_message,
            WebsocketActionEnum.GLOBAL_MESSAGE.value: self.handle_global_message,
        }

        self.perms = perms

        super().__init__(
            manager,
            QuizWebsocketPacketSchema,
            actions,
        )

    def handler(
        self,
        websocket: WebSocket,
        session_id: str,
        access_token: str,
    ):
        pool_id = session_id

        self.manager.check_auth(*self.perms)

        return super().handler(websocket, pool_id)

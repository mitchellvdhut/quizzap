"""Module containing the base websocket service for other variations to extend upon.
"""

# import os
from fastapi import WebSocket
from core.helpers.websocket import manager
from core.db.enums import WebsocketActionEnum
from core.helpers.websocket.schemas.packet import QuizWebsocketPacketSchema
from core.helpers.websocket.base import BaseWebsocketService
from core.helpers.websocket.permission.permission_dependency import PermList


class QuizWebsocketService(BaseWebsocketService):
    def __init__(
        self,
        websocket: WebSocket,
        perms: PermList | None = None,
    ):
        actions = {
            WebsocketActionEnum.POOL_MESSAGE.value: self.handle_pool_message,
            WebsocketActionEnum.GLOBAL_MESSAGE.value: self.handle_global_message,
        }

        self.perms = perms

        super().__init__(
            manager,
            websocket,
            QuizWebsocketPacketSchema,
            actions,
        )

    async def handler(
        self,
        quiz_id: int,
        session_id: str | None = None,
        access_token: str | None = None,
    ):
        await self.initialize()

        if not await self.manager.check_auth(
            *self.perms,
            pool_id=session_id,
            access_token=access_token,
        ):
            await self.handle_unautorized()
            await self.ws.close()
            return

        return await super().handler(
            pool_id=session_id,
            quiz_id=quiz_id,
        )

    async def process(
        self,
        **kwargs,
    ):
        del kwargs

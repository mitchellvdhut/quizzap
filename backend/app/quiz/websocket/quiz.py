"""Module containing the base websocket service for other variations to extend upon.
"""

import random
from fastapi import WebSocket
from app.user.services.user import UserService
from core.helpers.logger import log_exc
from core.exceptions.token import DecodeTokenException
from core.db.session import get_session
from core.helpers.hashids import decode_single
from core.helpers.token.token_helper import TokenHelper
from core.exceptions.websocket import SessionNotFoundException, SuccessfullConnection
from core.helpers.websocket import manager
from core.enums.websocket import QuizSessionActionEnum, WebsocketActionEnum
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
            WebsocketActionEnum.SESSION_CLOSE.value: self.handle_session_close,
            QuizSessionActionEnum.SUBMIT_VOTE: self.handle_action_not_implemented,
            QuizSessionActionEnum.QUESTION_INFO: self.handle_action_not_implemented,
            QuizSessionActionEnum.QUESTION_START: self.handle_action_not_implemented,
            QuizSessionActionEnum.QUESTION_STOP: self.handle_action_not_implemented,
            QuizSessionActionEnum.SCORE_INFO: self.handle_action_not_implemented,
        }

        super().__init__(
            manager,
            websocket,
            perms,
            QuizWebsocketPacketSchema,
            actions,
        )

    @log_exc
    async def start_create_session(
        self,
        quiz_id: int,
        access_token: str,
    ):
        await self.create_session()
        await self.manager.connect(self.ws, self.pool_id)

        if not await self.manager.check_auth(
            *self.perms,
            access_token=access_token,
        ):
            await self.handle_unautorized()
            await self.manager.disconnect(self.ws, self.pool_id)
            return

        @get_session
        async def get_user(session):
            try:
                info = TokenHelper.decode(token=access_token)
                user_id = decode_single(info["user_id"])

            except DecodeTokenException:
                user_id = 1

            return await UserService(session).get_user(user_id)

        user = await get_user()

        if not user:
            await self.handle_unautorized()
            await self.manager.disconnect(self.ws, self.pool_id)
            return

        data = {"username": user.username}

        self.manager.setdata(self.pool_id, self.ws.id, data)

        await self.ws.status_code(SuccessfullConnection)
        await self.handle_created_session(self.pool_id)

        await self.handler(quiz_id=quiz_id)

    @log_exc
    async def start_join_session(
        self,
        quiz_id: int,
        session_id: int,
        username: str,
    ):
        self.pool_id = session_id

        if not self.manager.active_pools.get(session_id):
            self.pool_id = "disconnect"
            await self.manager.connect(self.ws, self.pool_id)
            await self.handle_session_not_found()
            await self.manager.disconnect(self.ws, self.pool_id)
            return

        await self.manager.connect(self.ws, self.pool_id)

        if not await self.manager.check_auth(*self.perms):
            await self.handle_unautorized()
            await self.manager.disconnect(self.ws, self.pool_id)
            return

        data = {"username": username}

        self.manager.setdata(self.pool_id, self.ws.id, data)

        await self.ws.status_code(SuccessfullConnection)
        await self.handle_user_joined(username)

        await self.handler(quiz_id=quiz_id)

    async def process(
        self,
        **kwargs,
    ):
        del kwargs

    async def handle_user_joined(self, username: str):
        packet = QuizWebsocketPacketSchema(
            status_code=100,
            action=WebsocketActionEnum.USER_CONNECT,
            message="user has connected",
            payload={"username": username},
        )

        await self.manager.pool_packet(self.pool_id, packet)

    async def handle_session_not_found(self) -> None:
        await self.ws.status_code(SessionNotFoundException)

    async def create_session(self) -> None:
        while not self.pool_id or self.manager.active_pools.get(self.pool_id):
            self.pool_id = random.randint(100000, 999999)

    async def handle_created_session(self, session_id: int) -> None:
        packet = QuizWebsocketPacketSchema(
            status_code=201,
            action=QuizSessionActionEnum.SESSION_CREATED,
            message="created new session",
            payload={"session_id": session_id},
        )

        await self.ws.send(packet.model_dump())

    async def handle_pool_message(
        self,
        packet: QuizWebsocketPacketSchema,
        message: str | None = None,
        **kwargs,
    ) -> None:
        """Handle a message sent by a participant of a pool to the entire pool.

        Args:
            packet (SwipeSessionPacketSchema): WebsocketPacket sent by client.
            websocket (WebSocket): The websocket connection.

        Returns:
            None.
        """
        del kwargs

        packet.payload["username"] = self.manager.getdata(self.pool_id, self.ws.id)[
            "username"
        ]

        await super().handle_pool_message(packet, message)

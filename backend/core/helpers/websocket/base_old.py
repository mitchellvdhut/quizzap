import logging
from typing import Any, Type
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from app.quiz.schemas.websocket import GlobalMessageRequestSchema
from backend.core.helpers.websocket.classes.websocket import WebSocketConnection
from core.enums.websocket import WebSocketActionEnum
from core.exceptions.base import CustomException
from core.exceptions.websocket import (
    AccessDeniedException,
    ActionNotImplementedException,
    SuccessfullConnection,
)
from core.helpers.logger import get_logger
from core.helpers.websocket.schemas.packet import BaseWebSocketPacketSchema
from core.helpers.websocket.manager import WebSocketConnectionManager
from core.helpers.websocket.permission.permission_dependency import PermList


class BaseWebSocketService:
    def __init__(
        self,
        manager: WebSocketConnectionManager,
        websocket: WebSocket,
        perms: PermList | None = None,
        schema: Type[BaseWebSocketPacketSchema] = BaseWebSocketPacketSchema,
        actions: dict | None = None,
    ) -> None:
        self.manager = manager
        self.schema = schema
        self.perms = perms

        self.pool_id = None

        self.ws = WebSocketConnection(websocket)

        if not actions:
            self.actions = {
                WebSocketActionEnum.POOL_MESSAGE.value: self.handle_pool_message,
                WebSocketActionEnum.GLOBAL_MESSAGE.value: self.handle_global_message,
                WebSocketActionEnum.SESSION_CLOSE.value: self.handle_session_close,
            }
        else:
            self.actions = actions

    async def start(
        self,
        pool_id: int,
        **kwargs,
    ) -> None:
        self.pool_id = pool_id

        await self.manager.connect(self.ws, pool_id)
        await self.ws.status_code(SuccessfullConnection)

        await self.handler(pool_id, **kwargs)

    async def handler(self, **kwargs) -> None:
        try:
            while self.ws.is_connected:
                try:
                    packet: BaseWebSocketPacketSchema = await self.ws.listen(
                        self.schema,
                        timeout=0.1,
                    )

                except CustomException as exc:
                    await self.ws.status_code(exc)

                else:
                    if not packet:
                        await self.process(**kwargs)

                    else:
                        func = self.actions.get(
                            packet.action.value,
                            self.handle_action_not_implemented,
                        )

                        await func(
                            packet=packet,
                            **kwargs,
                        )

            await self.handle_disconnect()

        except WebSocketDisconnect:
            await self.handle_disconnect()

        except WebSocketException as exc:
            get_logger(exc)
            logging.info(self.active_pools)
            logging.info(f"pool_id {self.pool_id}, func: {func.__name__}")
            logging.info(self.active_pools.get(self.pool_id))
            logging.exception(exc)
            print(exc)

    async def process(
        self,
        **kwargs,
    ):
        del kwargs

    async def handle_disconnect(
        self,
        **kwargs,
    ) -> None:
        del kwargs

        # Check because sometimes the exception is raised
        # but it's already disconnected
        if self.ws.is_client_connected:
            await self.manager.disconnect(self.ws, self.pool_id)

        elif self.ws.is_application_connected:
            self.manager.remove_websocket(self.ws, self.pool_id)

        await self.handle_user_disconnect()

    async def handle_unautorized(self, **kwargs) -> None:
        del kwargs

        await self.ws.status_code(AccessDeniedException)

    async def handle_action_not_implemented(self, **kwargs) -> None:
        del kwargs

        await self.ws.status_code(ActionNotImplementedException)

    async def handle_global_message_request(
        self,
        packet: BaseWebSocketPacketSchema,
        **kwargs,
    ) -> None:
        del kwargs

        payload: GlobalMessageRequestSchema = self.ws.validate_payload(
            packet.payload,
            GlobalMessageRequestSchema,
        )

        if not payload:
            return

        await self.handle_global_message(payload.username)

    async def handle_global_message(
        self,
        username: str,
        **kwargs,
    ) -> None:
        del kwargs

        payload = {"username": username}

        await self.handle_global_message_response(payload)

    async def handle_global_message_response(
        self,
        payload: dict[str, Any],
        message: str | None = None,
        **kwargs,
    ) -> None:
        del kwargs

        packet = BaseWebSocketPacketSchema(
            status_code=200,
            message=message,
            action=WebSocketActionEnum.GLOBAL_MESSAGE,
            payload=payload,
        )

        await self.manager.global_packet(packet)

    async def response_global_message() -> None: ...

    async def handle_pool_message(
        self,
        packet: BaseWebSocketPacketSchema,
        message: str | None = None,
        **kwargs,
    ) -> None:
        del kwargs

        if not message:
            message = "message sent by user"

        packet = BaseWebSocketPacketSchema(
            status_code=200,
            message=message,
            action=WebSocketActionEnum.POOL_MESSAGE,
            payload=packet.payload,
        )

        await self.manager.pool_packet(self.pool_id, packet)

    async def handle_session_close(
        self,
        message: str | None = None,
        # payload: dict[str, str] | None = None,
        **kwargs,
    ) -> None:
        del kwargs

        if not message:
            message = "session is closing"

        packet = BaseWebSocketPacketSchema(
            status_code=200,
            message=message,
            action=WebSocketActionEnum.SESSION_CLOSE,
            # payload=payload
        )

        await self.manager.pool_packet(self.pool_id, packet)

        clients = self.manager.active_pools[self.pool_id]["clients"].values()
        for client in clients:
            await self.handle_user_disconnect(
                payload={"username": client["data"]["username"]}
            )

        await self.manager.pool_disconnect(self.pool_id)

    async def handle_user_disconnect(
        self,
        message: str | None = None,
        payload: dict[str, str] | None = None,
        **kwargs,
    ) -> None:
        del kwargs

        if not message:
            message = "user disconnected"

        packet = BaseWebSocketPacketSchema(
            status_code=200,
            message=message,
            action=WebSocketActionEnum.USER_DISCONNECT,
            payload=payload,
        )

        await self.manager.pool_packet(self.pool_id, packet)

    async def handle_user_connect(
        self,
        message: str | None = None,
        payload: dict[str, str] | None = None,
        **kwargs,
    ) -> None:
        del kwargs

        if not message:
            message = "user has connected"

        packet = BaseWebSocketPacketSchema(
            status_code=100,
            action=WebSocketActionEnum.USER_CONNECT,
            message=message,
            payload=payload,
        )

        await self.manager.pool_packet(self.pool_id, packet)

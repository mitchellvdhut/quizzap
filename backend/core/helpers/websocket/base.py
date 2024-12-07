"""Module containing the base websocket service for other variations to extend upon.
"""

import logging
from typing import Type
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from core.helpers.websocket.websocket import WebSocketConnection
from core.enums.websocket import WebsocketActionEnum
from core.exceptions.base import CustomException
from core.exceptions.websocket import (
    AccessDeniedException,
    ActionNotImplementedException,
    SuccessfullConnection,
)
from core.helpers.logger import get_logger
from core.helpers.websocket.schemas.packet import BaseWebsocketPacketSchema
from core.helpers.websocket.manager import WebSocketConnectionManager
from core.helpers.websocket.permission.permission_dependency import PermList


class BaseWebsocketService:
    def __init__(
        self,
        manager: WebSocketConnectionManager,
        websocket: WebSocket,
        perms: PermList | None = None,
        schema: Type[BaseWebsocketPacketSchema] = BaseWebsocketPacketSchema,
        actions: dict | None = None,
    ) -> None:
        self.manager = manager
        self.schema = schema
        self.perms = perms

        self.pool_id = None

        self.ws = WebSocketConnection(websocket)

        if not actions:
            self.actions = {
                WebsocketActionEnum.POOL_MESSAGE.value: self.handle_pool_message,
                WebsocketActionEnum.GLOBAL_MESSAGE.value: self.handle_global_message,
                WebsocketActionEnum.SESSION_CLOSE.value: self.handle_session_close,
            }
        else:
            self.actions = actions

    async def initialize(self):
        await self.ws.accept()

    async def start(
        self,
        pool_id: str,
        **kwargs,
    ) -> None:
        self.pool_id = pool_id

        await self.manager.connect(self.ws, pool_id)
        await self.ws.status_code(SuccessfullConnection)

        await self.handler(pool_id, **kwargs)

    async def handler(self, **kwargs) -> None:
        """The handler for the Websocket protocol.

        Args:
            websocket (WebSocket): The websocket connection.
            pool_id (int): The identifiër for which pool the websocket will be
            connected to.
            kwargs: Any extra arguments which will be passed to the functions ran by
            the handler.
        """
        try:
            while self.ws.is_connected:
                try:
                    packet: BaseWebsocketPacketSchema = await self.ws.listen(
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

            await self.finish()

        except WebSocketDisconnect:
            await self.finish()

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

    async def finish(self):
        logger = logging.getLogger("quizzap")
        logger.info("Websocket Disconnect")
        # Check because sometimes the exception is raised
        # but it's already disconnected
        if self.ws.is_client_connected:
            await self.manager.disconnect(self.ws, self.pool_id)

        elif self.ws.is_application_connected:
            self.manager.remove_websocket(self.ws, self.pool_id)

    async def handle_unautorized(self, **kwargs) -> None:
        del kwargs

        await self.ws.status_code(AccessDeniedException)

    async def handle_action_not_implemented(self, **kwargs) -> None:
        """Handle an action packet that has not been implemented.

        Args:
            websocket (WebSocket): The websocket connection.

        Returns:
            None.
        """
        del kwargs

        await self.ws.status_code(ActionNotImplementedException)

    async def handle_global_message(
        self,
        packet: BaseWebsocketPacketSchema,
        message: str | None = None,
        **kwargs,
    ) -> None:
        """Handle a global message sent by an admin user to all participants of a
        swipe session.

        Args:
            packet (SwipeSessionPacketSchema): WebsocketPacket sent by client.
            websocket (WebSocket): The websocket connection.

        Returns:
            None.
        """
        del kwargs

        if not message:
            message = "broadcasted message sent by user"

        packet = BaseWebsocketPacketSchema(
            status_code=200,
            message=message,
            action=WebsocketActionEnum.GLOBAL_MESSAGE,
            payload=packet.payload,
        )

        await self.manager.global_packet(packet)

    async def handle_pool_message(
        self,
        packet: BaseWebsocketPacketSchema,
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

        if not message:
            message = "message sent by user"

        packet = BaseWebsocketPacketSchema(
            status_code=200,
            message=message,
            action=WebsocketActionEnum.POOL_MESSAGE,
            payload=packet.payload,
        )

        await self.manager.pool_packet(self.pool_id, packet)

    async def handle_session_close(
        self,
        message: str | None = None,
        **kwargs,
    ) -> None:
        del kwargs

        if not message:
            message = "session is closing"

        packet = BaseWebsocketPacketSchema(
            status_code=200,
            message=message,
            action=WebsocketActionEnum.SESSION_CLOSE,
        )

        await self.manager.pool_packet(self.pool_id, packet)

        clients = self.manager.active_pools[self.pool_id]["clients"].values()
        for client in clients:
            await self.handle_user_disconnect(username=client["data"]["username"])

        await self.manager.pool_disconnect(self.pool_id)

    async def handle_user_disconnect(
        self,
        username: str | None = None,
        **kwargs,
    ) -> None:
        del kwargs

        if not username:
            username = self.manager.getdata(self.pool_id, self.ws.id)["username"]

        message = "user disconnected"
        payload = {"username": username}

        packet = BaseWebsocketPacketSchema(
            status_code=200,
            message=message,
            action=WebsocketActionEnum.USER_DISCONNECT,
            payload=payload
        )

        await self.manager.pool_packet(self.pool_id, packet)

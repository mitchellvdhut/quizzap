"""Module containing the base websocket service for other variations to extend upon.
"""

import logging
from typing import Type
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from starlette.websockets import WebSocketState
from core.helpers.websocket.websocket import WebSocketConnection
from core.db.enums import WebsocketActionEnum
from core.exceptions.base import CustomException
from core.exceptions.websocket import (
    AccessDeniedException,
    ActionNotImplementedException,
    SuccessfullConnection,
)
from core.helpers.logger import get_logger
from core.helpers.websocket.schemas.packet import BaseWebsocketPacketSchema
from core.helpers.websocket.manager import WebSocketConnectionManager


class BaseWebsocketService:
    async def __init__(
        self,
        manager: WebSocketConnectionManager,
        websocket: WebSocket,
        schema: Type[BaseWebsocketPacketSchema] = BaseWebsocketPacketSchema,
        actions: dict = None,
    ) -> None:
        self.manager = manager
        self.schema = schema

        self.pool_id = None

        self.ws = await WebSocketConnection(websocket)

        if not actions:
            self.actions = {
                WebsocketActionEnum.POOL_MESSAGE.value: self.handle_pool_message,
                WebsocketActionEnum.GLOBAL_MESSAGE.value: self.handle_global_message,
            }
        else:
            self.actions = actions

    async def handler(
        self,
        pool_id: str,
        **kwargs,
    ) -> None:
        """The handler for the Websocket protocol.

        Args:
            websocket (WebSocket): The websocket connection.
            pool_id (int): The identifiër for which pool the websocket will be
            connected to.
            kwargs: Any extra arguments which will be passed to the functions ran by
            the handler.
        """
        self.pool_id = pool_id

        await self.manager.connect(self.ws, pool_id)
        await self.manager.handle_connection_code(self.ws, SuccessfullConnection)

        try:
            while (
                self.ws.application_state == WebSocketState.CONNECTED
                and self.ws.client_state == WebSocketState.CONNECTED
            ):
                try:
                    packet: BaseWebsocketPacketSchema = await self.ws.listen(
                        self.schema,
                        timeout=0.1,
                    )

                except CustomException as exc:
                    await self.manager.handle_connection_code(
                        self.ws,
                        exc,
                    )

                else:
                    if not packet:
                        await self.process()

                    else:
                        func = self.actions.get(
                            packet.action.value,
                            self.handle_action_not_implemented,
                        )

                        await func(
                            packet=packet,
                            **kwargs,
                        )

        except WebSocketDisconnect:
            # Check because sometimes the exception is raised
            # but it's already disconnected
            if self.ws.client_state == WebSocketState.CONNECTED:
                await self.manager.disconnect(self.ws, pool_id)

            elif self.ws.application_state == WebSocketState.CONNECTED:
                self.manager.remove_websocket(self.ws, pool_id)

        except WebSocketException as exc:
            get_logger(exc)
            logging.info(self.active_pools)
            logging.info(f"pool_id {pool_id}, func: {func.__name__}")
            logging.info(self.active_pools.get(pool_id))
            logging.exception(exc)
            print(exc)

    async def process(
        self,
        **kwargs,
    ):
        del kwargs

    async def handle_unautorized(
        self,
        **kwargs,
    ):
        del kwargs

        await self.manager.handle_connection_code(
            self.ws,
            AccessDeniedException,
        )
    
    async def handle_action_not_implemented(
        self,
        **kwargs,
    ):
        """Handle an action packet that has not been implemented.

        Args:
            websocket (WebSocket): The websocket connection.

        Returns:
            None.
        """
        del kwargs

        await self.manager.handle_connection_code(
            self.ws,
            ActionNotImplementedException,
        )

    async def handle_global_message(
        self,
        packet: BaseWebsocketPacketSchema,
        **kwargs,
    ):
        """Handle a global message sent by an admin user to all participants of a
        swipe session.

        Args:
            packet (SwipeSessionPacketSchema): WebsocketPacket sent by client.
            websocket (WebSocket): The websocket connection.

        Returns:
            None.
        """
        del kwargs

        await self.manager.handle_global_message(
            self.ws,
            packet.payload.get("message"),
        )

    async def handle_pool_message(
        self,
        packet: BaseWebsocketPacketSchema,
        **kwargs,
    ):
        """Handle a message sent by a participant of a pool to the entire pool.

        Args:
            pool_id (int): Identifier for the pool to send the message to.
            packet (SwipeSessionPacketSchema): WebsocketPacket sent by client.
            websocket (WebSocket): The websocket connection.

        Returns:
            None.
        """
        del kwargs

        await self.manager.handle_pool_message(
            self.ws,
            self.pool_id,
            packet.payload.get("message"),
        )

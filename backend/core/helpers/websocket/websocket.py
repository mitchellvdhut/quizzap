import asyncio
import json
import logging
from typing import Any, Type
from fastapi import WebSocket
from fastapi.websockets import WebSocketState
from pydantic import ValidationError

from core.db.enums import WebsocketActionEnum
from core.exceptions.base import CustomException
from core.exceptions.websocket import ActionNotFoundException, JSONSerializableException
from core.helpers.websocket.schemas.packet import BaseWebsocketPacketSchema


class WebSocketConnection:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.accepted = False

    @property
    def id(self):
        return id(self.websocket)

    async def accept(self) -> None:
        if not self.accepted:
            await self.websocket.accept()
            self.accepted = True

    async def send(
        self,
        data: dict[str, Any],
    ):
        print("WEBSOCKET SENDING:", data)
        if self.is_connected:
            await self.websocket.send_json(data)

    async def listen(
        self,
        schema: Type[BaseWebsocketPacketSchema],
        timeout: float | None = None,
    ) -> BaseWebsocketPacketSchema | None:
        if timeout:
            try:
                data = await asyncio.wait_for(
                    self.websocket.receive_text(),
                    timeout=timeout,
                )
                logger = logging.getLogger("quizzap")
                logger.info(data)

            except asyncio.TimeoutError:
                return None

        else:
            data = await self.websocket.receive_text()

        try:
            data_json = json.loads(data)
        except json.decoder.JSONDecodeError as exc:
            raise JSONSerializableException from exc

        try:
            packet = schema(**data_json)
        except ValidationError as exc:
            raise ActionNotFoundException from exc

        return packet

    async def status_code(
        self,
        exception: CustomException,
    ) -> None:
        if not self.accepted:
            raise Exception("WebSocket was not accepted.")

        packet = BaseWebsocketPacketSchema(
            action=WebsocketActionEnum.STATUS_CODE,
            status_code=exception.status_code,
            message=exception.message,
            payload=None,
        )

        await self.send(packet.model_dump())

    @property
    def is_connected(self):
        return self.websocket.client_state == WebSocketState.CONNECTED and self.websocket.application_state == WebSocketState.CONNECTED

    @property
    def is_client_connected(self):
        return self.websocket.client_state == WebSocketState.CONNECTED

    @property
    def is_application_connected(self):
        return self.websocket.application_state == WebSocketState.CONNECTED
    
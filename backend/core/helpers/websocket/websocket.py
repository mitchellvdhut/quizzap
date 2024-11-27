import asyncio
import json
from typing import Any, Type
from fastapi import WebSocket
from fastapi.websockets import WebSocketState
from pydantic import ValidationError

from core.db.enums import WebsocketActionEnum
from core.exceptions.base import CustomException
from core.exceptions.websocket import ActionNotFoundException, JSONSerializableException
from core.helpers.websocket.schemas.packet import BaseWebsocketPacketSchema


class WebSocketConnection(WebSocket):
    def __init__(self, websocket: WebSocket):
        self.ws = websocket

    @property
    def id(self):
        return id(self.websocket)

    async def send(
        self,
        data: dict[str, Any],
    ):
        print("WEBSOCKET SENDING:", data)
        if (
            self.ws.client_state == WebSocketState.CONNECTED
            and self.ws.application_state == WebSocketState.CONNECTED
        ):
            await self.ws.send_json(data)

    async def listen(
        self,
        schema: Type[BaseWebsocketPacketSchema],
        timeout: float | None = None,
    ) -> BaseWebsocketPacketSchema | None:
        if timeout:
            try:
                data = await asyncio.wait_for(
                    self.ws.receive_text(),
                    timeout=timeout,
                )

            except asyncio.TimeoutError:
                return None
        else:
            data = await self.ws.receive_text()

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
        packet = BaseWebsocketPacketSchema(
            action=WebsocketActionEnum.STATUS_CODE,
            status_code=exception.status_code,
            message=exception.message,
            payload=None,
        )

        await self.send(packet)

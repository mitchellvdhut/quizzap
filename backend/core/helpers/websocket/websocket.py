import asyncio
import datetime
import json
import logging
from typing import Type
import uuid
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from pydantic import BaseModel, ValidationError

from core.enums.websocket import WebsocketActionEnum
from core.exceptions.base import CustomException
from core.exceptions.websocket import ActionNotImplementedException, JSONSerializableException
from core.helpers.websocket.schemas.packet import BaseWebsocketPacketSchema


class WebSocketConnection:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.accepted = False

    @property
    def id(self):
        return id(self.websocket)

    async def accept(self, *args, **kwargs) -> None:
        if not self.accepted:
            await self.websocket.accept(*args, **kwargs)
            self.accepted = True

    async def close(self, *args, **kwargs) -> None:
        if self.accepted:
            await self.websocket.close(*args, **kwargs)
            self.accepted = False

    async def send(
        self,
        data: BaseWebsocketPacketSchema,
    ):
        if not self.is_connected:
            return
        print("WEBSOCKET SENDING:", data)

        def default(o):
            if isinstance(o, (datetime.date, datetime.datetime)):
                return o.isoformat()
            
            if isinstance(o, uuid.UUID):
                return str(o)
            
            if isinstance(o, BaseModel):
                return o.model_dump()

        data = json.dumps(data, default=default)

        await self.websocket.send_text(data)

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
                logger.info(f"Incoming request: {data=}")

            except asyncio.TimeoutError:
                return None
            
            except WebSocketDisconnect:
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
            raise ActionNotImplementedException from exc

        return packet

    async def status_code(
        self,
        exception: CustomException,
    ) -> None:
        if not self.accepted:
            raise Exception("WebSocket was not accepted.")

        packet = BaseWebsocketPacketSchema(
            status_code=exception.status_code,
            action=WebsocketActionEnum.STATUS_CODE,
            message=exception.message,
            payload=None,
        )

        await self.send(packet)

    @property
    def is_connected(self):
        return self.websocket.client_state == WebSocketState.CONNECTED and self.websocket.application_state == WebSocketState.CONNECTED

    @property
    def is_client_connected(self):
        return self.websocket.client_state == WebSocketState.CONNECTED

    @property
    def is_application_connected(self):
        return self.websocket.application_state == WebSocketState.CONNECTED
    
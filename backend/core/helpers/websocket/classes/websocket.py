import asyncio
import datetime
import json
import logging
from typing import Type
import uuid
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from pydantic import BaseModel, ValidationError

from core.enums.websocket import WebSocketActionEnum
from core.exceptions.base import CustomException
from core.exceptions.websocket import (
    ActionNotImplementedException,
    IncompletePayloadException,
    JSONSerializableException,
)
from core.helpers.websocket.schemas.packet import WebSocketPacketSchema


class WebSocketConnection:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.accepted = False
        self.disconnected = False

    @property
    def id(self):
        return id(self.websocket)

    async def accept(self, *args, **kwargs) -> None:
        if not self.accepted:
            await self.websocket.accept(*args, **kwargs)
            self.accepted = True

    async def close(self, *args, **kwargs) -> None:
        if self.accepted and self.is_connected:
            await self.websocket.close(*args, **kwargs)
            self.accepted = False

    async def disconnect(self, *args, **kwargs) -> None:
        await self.close(*args, **kwargs)
        self.websocket = None
        self.accepted = False
        self.disconnected = True

    async def reconnect(self, websocket: WebSocket, *args, **kwargs):
        self.websocket = websocket
        self.disconnected = False
        await self.accept(*args, **kwargs)

    async def send(
        self,
        data: WebSocketPacketSchema,
    ):
        logger = logging.getLogger("quizzap")

        if not self.is_connected:
            logger.warning("Trying to send to disconnected websocket")
            return

        logger.info(f"WebSocket Sending: {data}")

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
        schema: Type[WebSocketPacketSchema],
        timeout: float | None = None,
    ) -> WebSocketPacketSchema | None:
        if self.disconnected:
            logger = logging.getLogger("quizzap")
            logger.warning("Trying to listen to disconnected websocket")
            return

        if timeout:
            try:
                data = await asyncio.wait_for(
                    self.websocket.receive_text(),
                    timeout=timeout,
                )

                logger = logging.getLogger("quizzap")
                logger.info(f"Incoming request: {data}")

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
    
    def validate_payload(self, packet: WebSocketPacketSchema, schema: Type[BaseModel]) -> Type[BaseModel] | None:
        try:
            payload = schema(**packet.payload)
        except ValidationError as exc:
            self.status_code(IncompletePayloadException(str(exc.errors())))
            return

        return payload

    async def status_code(
        self,
        exception: CustomException,
    ) -> None:
        if not self.accepted:
            raise Exception("WebSocket was not accepted.")

        packet = WebSocketPacketSchema(
            status_code=exception.status_code,
            action=WebSocketActionEnum.STATUS_CODE,
            message=exception.message,
            payload=None,
        )

        await self.send(packet)

    @property
    def is_connected(self):
        return (
            not self.disconnected
            and self.websocket.client_state == WebSocketState.CONNECTED
            and self.websocket.application_state == WebSocketState.CONNECTED
        )

    @property
    def is_client_connected(self):
        return (
            not self.disconnected
            and self.websocket.client_state == WebSocketState.CONNECTED
        )

    @property
    def is_application_connected(self):
        return (
            not self.disconnected
            and self.websocket.application_state == WebSocketState.CONNECTED
        )

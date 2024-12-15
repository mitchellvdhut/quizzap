from abc import ABC, abstractmethod
from typing import Type
from pydantic import BaseModel

from core.enums.websocket import WebSocketTargetEnum, WebSocketActionEnum
from core.helpers.websocket.classes.websocket import WebSocketConnection
from core.helpers.websocket.schemas.packet import BaseWebSocketPacketSchema, WebSocketPacketSchema
from core.helpers.websocket.manager import WebSocketConnectionManager


class WebSocketCommand(ABC):
    request_schema: BaseModel | None
    response_schema: BaseModel | None
    target: WebSocketTargetEnum = WebSocketTargetEnum.INDIVIDUAL
    action: WebSocketActionEnum = WebSocketActionEnum.STATUS_CODE
    status_code: int = 200
    message: str = "successfully executed"

    def __init__(
        self,
        manager: WebSocketConnectionManager,
        ws: WebSocketConnection,
    ) -> None:
        self.manager = manager
        self.ws = ws

    def set_message(self, message: str) -> None:
        self.message = message

    async def request(
        self,
        packet: BaseWebSocketPacketSchema,
    ) -> None:
        if self.request_schema is None:
            await self._handle()
            return

        payload = self.ws.validate_payload(packet, self.request_schema)

        if not payload:
            return

        await self._handle(payload)

    async def _handle(self, payload: Type[BaseModel] | None = None) -> None:
        response_payload = await self.handle(payload)
        await self.response(response_payload)

    @abstractmethod
    async def handle(self, payload: Type[BaseModel]) -> Type[BaseModel]:
        """
        Processes the given payload and returns a response payload.
        """

    async def response(self, payload: Type[BaseModel] | None = None) -> None:
        if payload is not None and not isinstance(payload, self.response_schema):
            raise ValueError(f"Payload is not of type {self.response_schema}")
        
        packet = WebSocketPacketSchema(
            action=self.action,
            status_code=self.status_code,
            message=self.message,
            payload=payload,
        )

        match self.target:
            case WebSocketTargetEnum.INDIVIDUAL:
                await self.ws.send(packet)

            case WebSocketTargetEnum.POOL:
                pool_id = self.manager.get_client_pool(self.ws.id)
                await self.manager.pool_packet(pool_id)

            case WebSocketTargetEnum.GLOBAL:
                await self.manager.global_packet(packet)

            case _:
                raise Exception("No specified target")


WebSocketCommand()

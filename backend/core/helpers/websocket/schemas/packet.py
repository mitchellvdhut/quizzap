from enum import Enum
from typing import Any
from pydantic import BaseModel

from core.enums.websocket import QuizSessionActionEnum, WebSocketActionEnum


class WebSocketPacketSchema(BaseModel):
    status_code: int | None = None
    action: Enum
    message: str
    payload: dict[str, Any] | None = None


class BaseWebSocketPacketSchema(WebSocketPacketSchema):
    action: WebSocketActionEnum


class QuizWebSocketPacketSchema(BaseWebSocketPacketSchema):
    action: WebSocketActionEnum | QuizSessionActionEnum

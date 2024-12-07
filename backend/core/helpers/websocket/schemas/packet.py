from typing import Any
from pydantic import BaseModel

from core.enums.websocket import QuizSessionActionEnum, WebsocketActionEnum


class BaseWebsocketPacketSchema(BaseModel):
    status_code: int | None = None
    action: WebsocketActionEnum
    message: str
    payload: dict[str, Any] | None = None


class QuizWebsocketPacketSchema(BaseWebsocketPacketSchema):
    action: WebsocketActionEnum | QuizSessionActionEnum

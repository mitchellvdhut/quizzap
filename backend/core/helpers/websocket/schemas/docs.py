from typing import Any
from pydantic import BaseModel


class WebSocketPacketParams(BaseModel):
    status_code: str = "integer"
    message: str = "string"
    action: str = "string"
    payload: dict[str, Any] = {}


class RequestWebSocketDocsSchema(BaseModel):
    info: str
    params: WebSocketPacketParams = WebSocketPacketParams(payload={})


class ResponseWebSocketDocsSchema(BaseModel):
    info: str
    params: WebSocketPacketParams = WebSocketPacketParams(payload={})


class WebSocketDocsSchema(BaseModel):
    info: str
    request: RequestWebSocketDocsSchema | None = None
    response: ResponseWebSocketDocsSchema | None = None

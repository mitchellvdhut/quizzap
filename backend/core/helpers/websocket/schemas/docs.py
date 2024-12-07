from typing import Any
from pydantic import BaseModel


class WebsocketPacketParams(BaseModel):
    status_code: str = "integer"
    message: str = "integer"
    action: str = "string"
    payload: str | dict[str, Any] = {}


class RequestWebsocketDocsSchema(BaseModel):
    info: str
    params: WebsocketPacketParams | None = None


class ResponseWebsocketDocsSchema(BaseModel):
    info: str
    params: WebsocketPacketParams | None = None


class WebsocketDocsSchema(BaseModel):
    info: str
    request: RequestWebsocketDocsSchema | None = None
    response: ResponseWebsocketDocsSchema | None = None

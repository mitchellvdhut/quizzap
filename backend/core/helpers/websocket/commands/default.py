from pydantic import BaseModel
from core.enums.websocket import WebSocketTargetEnum, WebSocketActionEnum
from core.helpers.websocket.classes.command import WebSocketCommand


class DefaultRequestSchema(BaseModel):
    ...


class DefaultResponeSchema(BaseModel):
    ...


class DefaultCommand(WebSocketCommand):
    request_schema = DefaultRequestSchema
    response_schema = DefaultResponeSchema
    action = WebSocketActionEnum.STATUS_CODE
    target = WebSocketTargetEnum.INDIVIDUAL
    message = "action does not exist or is not implemented"

    def handle(self, payload: DefaultRequestSchema | None = None) -> DefaultResponeSchema:
        del payload
        return None

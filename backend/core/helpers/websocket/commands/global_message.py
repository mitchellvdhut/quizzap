from pydantic import BaseModel
from core.enums.websocket import WebSocketTargetEnum, WebSocketActionEnum
from core.helpers.websocket.classes.command import WebSocketCommand


class GlobalMessageRequestSchema(BaseModel):
    message: str


class GlobalMessageResponeSchema(BaseModel):
    message: str


class GlobalMessageCommand(WebSocketCommand):
    request_schema = GlobalMessageRequestSchema
    response_schema = GlobalMessageResponeSchema
    action = WebSocketActionEnum.GLOBAL_MESSAGE
    target = WebSocketTargetEnum.GLOBAL
    message = "globally broadcasted message"

    def handle(self, payload: GlobalMessageRequestSchema) -> GlobalMessageResponeSchema:
        payload = GlobalMessageResponeSchema(
            message=payload.message
        )
        return payload

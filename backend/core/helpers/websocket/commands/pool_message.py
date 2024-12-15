from pydantic import BaseModel
from core.enums.websocket import WebSocketTargetEnum, WebSocketActionEnum
from core.helpers.websocket.classes.command import WebSocketCommand


class PoolMessageRequestSchema(BaseModel):
    message: str


class PoolMessageResponeSchema(BaseModel):
    message: str


class PoolMessageCommand(WebSocketCommand):
    request_schema = PoolMessageRequestSchema
    response_schema = PoolMessageResponeSchema
    action = WebSocketActionEnum.POOL_MESSAGE
    target = WebSocketTargetEnum.POOL
    message = "a pool message"

    def handle(self, payload: PoolMessageRequestSchema) -> PoolMessageResponeSchema:
        payload = PoolMessageResponeSchema(
            message=payload.message
        )
        self.set_message("message sent by user")
        return payload

from core.helpers.websocket.classes.state import BaseClientConnection, BaseClientData, BaseStateData, BaseWebSocketState
from core.helpers.websocket.classes.websocket import WebSocketConnection


class QuizStateData(BaseStateData):
    ...


class QuizClientData(BaseClientData):
    ...


class QuizClientConnection(BaseClientConnection):
    ws: WebSocketConnection
    data: QuizClientData


class QuizWebSocketState(BaseWebSocketState):
    ...

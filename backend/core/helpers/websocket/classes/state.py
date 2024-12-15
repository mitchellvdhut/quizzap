from abc import ABC
from typing import TypedDict

from core.helpers.websocket.classes.websocket import WebSocketConnection


class BaseStateData(TypedDict):
    ...


class BaseClientData(TypedDict):
    ...


class BaseClientConnection(TypedDict):
    ws: WebSocketConnection
    data: BaseClientData


class BaseWebSocketState(ABC):
    state_id: str
    clients: dict[int, BaseClientConnection]
    data: BaseStateData

    def __init__(self, state_id: str):
        self.state_id = state_id

    def set_client(self, websocket: WebSocketConnection, data: BaseClientData) -> None:
        self.clients[websocket.id] = {
            "data": data,
            "ws": websocket
        }

    def get_client(self, client_id: int) -> BaseClientConnection:
        return self.clients.get(client_id)

    def set_client_data(self, client_id: int, data: BaseClientData) -> None:
        self.clients[client_id]['data'] = data
    
    def get_client_data(self, client_id: int) -> BaseClientData:
        return self.clients[client_id]['data']

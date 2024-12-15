import logging
from typing import Any, TypedDict
from core.helpers.websocket.classes.websocket import WebSocketConnection


class ClientConnection(TypedDict):
    number: int
    ws: WebSocketConnection
    data: dict[str, Any]


class Pool(TypedDict):
    clients: dict[int, ClientConnection]
    amount: int
    data: dict[str, Any]


logger = logging.getLogger("quizzap")

class ActivePools(dict[str, Pool]):
    def create(self, identifier: str) -> None:
        self[identifier] = {"clients": {}, "amount": 0, "data": {}}

    def append(self, identifier: str, ws: WebSocketConnection) -> None:
        if not self.get(identifier):
            self.create(identifier)

        self[identifier]["amount"] += 1

        self[identifier]["clients"][ws.id] = {
            "ws": ws,
            "number": self[identifier]["amount"],
            "data": {}
        }

    def remove_pool(self, identifier: str) -> None:
        if not self.get(identifier):
            return
        
        self.pop(identifier)

    def remove(self, identifier: str, ws: WebSocketConnection) -> None:
        if not self.get(identifier):
            return

        for client_id in self[identifier]["clients"]:
            if client_id == ws.id:
                del self[identifier]["clients"][client_id]
                break

        if self.get_connection_count(identifier) < 1:
            self.pop(identifier)

    def set_data(self, pool_identifier: str, data: dict[str, Any]):
        self[pool_identifier]["data"] = data

    def get_data(self, pool_identifier: str):
        return self[pool_identifier]["data"]

    def set_client_data(self, pool_identifier: str, ws_identifier: int, data: dict[str, Any]):
        self[pool_identifier]["clients"][ws_identifier]["data"] = data

    def get_client_data(self, pool_identifier: str, ws_identifier: int):
        return self[pool_identifier]["clients"][ws_identifier]["data"]

    def get_connection_count(self, identifier: str | None = None) -> int:
        if identifier:
            if (pool := self.get(identifier)) is None:
                return 0

            return len(pool["clients"])

        total = 0
        for _, pool in self.items():
            total += len(pool["clients"])

        return total

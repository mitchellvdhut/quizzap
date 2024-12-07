from typing import Any, TypedDict
from core.helpers.websocket.websocket import WebSocketConnection


class ClientConnection(TypedDict):
    number: int
    ws: WebSocketConnection
    data: dict[str, Any]


class Pool(TypedDict):
    clients: dict[int, ClientConnection]
    amount: int


class ActivePools(dict[str, Pool]):
    def create(self, identifier: str) -> None:
        self[identifier] = {"clients": {}, "amount": 0}

    def append(self, identifier: str, ws: WebSocketConnection) -> None:
        if not self.get(identifier):
            self.create(identifier)

        self[identifier]["amount"] += 1

        self[identifier]["clients"][ws.id] = {
            "ws": ws,
            "number": self[identifier]["amount"],
            "data": {}
        }

    def remove(self, identifier: str, ws: WebSocketConnection) -> None:
        if not self.get(identifier):
            return

        for client_id, client in self[identifier]["clients"].items():
            if client_id == ws.id:
                del self[identifier]["clients"][client_id]
                break

        if self.get_connection_count(identifier) < 1:
            self.pop(identifier)

    def setdata(self, pool_identifier: str, ws_identifier: int, data: dict[str, Any]):
        self[pool_identifier]["clients"][ws_identifier]["data"] = data

    def getdata(self, pool_identifier: str, ws_identifier: int):
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

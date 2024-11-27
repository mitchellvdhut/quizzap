from typing import TypedDict
from backend.core.helpers.websocket.websocket import WebSocketConnection


class ClientConnection(TypedDict):
    number: int
    ws: WebSocketConnection


class Pool(TypedDict):
    clients: list[ClientConnection]
    amount: int


class ActivePools(dict[str, Pool]):
    def create(self, identifier: str) -> None:
        self[identifier] = {"clients": [], "amount": 0}

    def append(self, identifier: str, ws: WebSocketConnection) -> None:
        if not self.get(identifier):
            self.create(identifier)

        self[identifier]["amount"] += 1

        self[identifier]["clients"].append(
            {
                "ws": ws,
                "number": self[identifier]["amount"]
            }
        )

    def remove(self, identifier: str, ws: WebSocketConnection) -> None:
        if not self.get(identifier):
            return
        
        for client in self[identifier]["clients"]:
            if client["ws"].id == ws.id:
                self[identifier]["clients"].remove(client)
                break
        
        if self.get_connection_count(identifier) < 1:
            self.pop(identifier)

    def get_connection_count(self, identifier: str | None = None) -> int:
        if identifier:
            if (pool := self.get(identifier)) is None:
                return 0
            
            return len(pool["clients"])

        total = 0
        for _, pool in self.items():
            total += len(pool["clients"])

        return total

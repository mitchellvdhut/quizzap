from typing import Any, Type

from core.exceptions.websocket import AccessDeniedException
from core.helpers.websocket.active_pools import ActivePools
from core.exceptions.base import CustomException
from core.helpers.websocket.permission.permission_dependency import (
    WebsocketPermission,
    PermItem,
)
from core.helpers.websocket.schemas.packet import BaseWebsocketPacketSchema
from core.helpers.websocket.websocket import WebSocketConnection
from fastapi import status


class WebSocketConnectionManager:
    def __init__(self, *perms: PermItem):
        self.active_pools = ActivePools()
        self.perms = perms

    async def check_auth(
        self,
        *perms: PermItem,
        **kwargs,
    ):
        if not perms:
            perms = self.perms

        perm_checker = WebsocketPermission(perms)

        try:
            await perm_checker(**kwargs)

        except CustomException as exc:
            return exc

        return None

    async def connect(
        self,
        websocket: WebSocketConnection,
        pool_id: str,
    ) -> WebSocketConnection:
        await websocket.accept()
        self.active_pools.append(pool_id, websocket)
        return websocket

    async def send_data(
        self,
        websocket: WebSocketConnection,
        data: dict[str, Any],
    ) -> None:
        return await websocket.send(data)

    async def receive_data(
        self,
        websocket: WebSocketConnection,
        schema: Type[BaseWebsocketPacketSchema],
        timeout: float | None = None,
    ) -> BaseWebsocketPacketSchema | None:
        return await websocket.listen(schema, timeout)

    async def deny(
        self,
        websocket: WebSocketConnection,
        exception: CustomException = AccessDeniedException(),
    ) -> None:
        await websocket.accept()
        await websocket.status_code(exception)
        await websocket.close(status.WS_1000_NORMAL_CLOSURE)

    def remove_websocket(
        self,
        websocket: WebSocketConnection,
        pool_id: str,
    ):
        self.active_pools.remove(pool_id, websocket)

    async def disconnect(
        self,
        websocket: WebSocketConnection,
        pool_id: str,
    ):
        await websocket.close(status.WS_1000_NORMAL_CLOSURE)
        self.remove_websocket(websocket, pool_id)

    async def pool_disconnect(
        self,
        pool_id: str,
    ) -> None:
        pool = self.active_pools.get(pool_id)

        if not pool:
            print("Tried to disconnect from non existing pool")
            print(f"pool_id: {pool_id}", pool_id)
            print(f"manager object: {self.__dict__}")
            return

        connections = [ws for ws in pool["clients"]]

        for client in connections:
            await self.disconnect(client["websocket"], pool_id)

    async def personal_packet(
        self,
        websocket: WebSocketConnection,
        packet: BaseWebsocketPacketSchema,
    ) -> None:
        await websocket.send(packet.model_dump())

    async def pool_packet(
        self,
        pool_id: str,
        packet: BaseWebsocketPacketSchema,
    ) -> None:
        for client in self.active_pools[pool_id]["clients"]:
            await self.send_data(client["websocket"], packet.model_dump())

    async def global_packet(
        self,
        packet: BaseWebsocketPacketSchema,
    ) -> None:
        for _, pool in self.active_pools.items():
            for client in pool["clients"]:
                await self.send_data(
                    client["websocket"],
                    packet.model_dump(),
                )

    def get_connection_count(
        self,
        pool_id: str | None = None,
    ) -> int:
        return self.active_pools.get_connection_count(pool_id)

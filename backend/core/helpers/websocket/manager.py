import logging
from typing import Any
from core.helpers.websocket.active_pools import ActivePools
from core.exceptions.base import UnauthorizedException
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
        access_token: str | None = None,
        **kwargs,
    ):
        if not perms:
            perms = self.perms

        perm_checker = WebsocketPermission(perms)

        try:
            await perm_checker(access_token, **kwargs)

        except UnauthorizedException:
            return False

        return True

    async def connect(
        self,
        websocket: WebSocketConnection,
        pool_id: int,
    ) -> None:
        await websocket.accept()
        self.active_pools.append(pool_id, websocket)

    async def disconnect(
        self,
        websocket: WebSocketConnection,
        pool_id: int,
    ) -> None:
        await websocket.close(status.WS_1000_NORMAL_CLOSURE)
        self.remove_websocket(websocket, pool_id)

    def remove_websocket(
        self,
        websocket: WebSocketConnection,
        pool_id: int,
    ) -> None:
        self.active_pools.remove(pool_id, websocket)

    async def pool_disconnect(
        self,
        pool_id: int,
    ) -> None:
        pool = self.active_pools.get(pool_id)

        if not pool:
            logger = logging.getLogger("quizzap")
            logger.warning(f"Tried to disconnect from non existing pool: {pool_id}")
            return

        clients = [i for i in pool["clients"].values()]

        for client in clients:
            await self.disconnect(client["ws"], pool_id)

    async def personal_packet(
        self,
        websocket: WebSocketConnection,
        packet: BaseWebsocketPacketSchema,
    ) -> None:
        await websocket.send(packet)

    async def pool_packet(
        self,
        pool_id: int,
        packet: BaseWebsocketPacketSchema,
    ) -> None:
        for _, client in self.active_pools[pool_id]["clients"].items():
            await client["ws"].send(packet)

    async def global_packet(
        self,
        packet: BaseWebsocketPacketSchema,
    ) -> None:
        for _, pool in self.active_pools.items():
            for _, client in pool["clients"].items():
                await client["ws"].send(packet)

    def get_connection_count(
        self,
        pool_id: int | None = None,
    ) -> int:
        return self.active_pools.get_connection_count(pool_id)

    def set_data(
        self,
        pool_id: int,
        data: dict[str, Any],
    ) -> None:
        self.active_pools.set_data(pool_id, data)

    def get_data(
        self,
        pool_id: int,
    ) -> dict[str, Any]:
        return self.active_pools.get_data(pool_id)

    def set_client_data(
        self,
        pool_id: int,
        websocket_id: int,
        data: dict[str, Any],
    ) -> None:
        self.active_pools.set_client_data(pool_id, websocket_id, data)

    def get_client_data(
        self,
        pool_id: int,
        websocket_id: int,
    ) -> dict[str, Any]:
        return self.active_pools.get_client_data(pool_id, websocket_id)

    def garbage_collector(
        self, 
        pool_id: str | None = None,
    ) -> None:
        if pool_id:
            for _, client in self.active_pools[pool_id]["clients"].items():
                if client["ws"].is_connected:
                    break
            else:
                self.active_pools.remove_pool(pool_id)
            
            return
        
        for pool_id in self.active_pools:
            for _, client in self.active_pools[pool_id]["clients"].items():
                if client["ws"].is_connected:
                    break
            else:
                self.active_pools.remove_pool(pool_id)

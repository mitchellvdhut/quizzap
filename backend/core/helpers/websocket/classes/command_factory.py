from core.helpers.websocket.schemas.packet import BaseWebSocketPacketSchema
from core.enums.websocket import WebSocketActionEnum
from core.helpers.websocket.classes.command import WebSocketCommand
from core.helpers.websocket.classes.websocket import WebSocketConnection
from core.helpers.websocket.manager import WebSocketConnectionManager


class WebSocketCommandRegistry:
    def __init__(
        self,
        manager: WebSocketConnectionManager,
        default: type[WebSocketCommand],
    ):
        self.manager = manager
        self.commands: dict[type[WebSocketActionEnum], type[WebSocketCommand]] = {}
        self.default = default

    def register(
        self,
        command: type[WebSocketCommand],
    ) -> type[WebSocketCommand]:
        self.commands[command.action] = command

    def retrieve(
        self,
        action: type[WebSocketActionEnum],
    ) -> type[WebSocketActionEnum] | None:
        return self.commands.get(action)

    async def execute(
        self,
        action: type[WebSocketActionEnum],
        ws: WebSocketConnection,
        packet: type[BaseWebSocketPacketSchema]
    ) -> None:
        command = self.commands.get(action, self.default)
        command = command(self.manager, ws)
        await command.request(packet)

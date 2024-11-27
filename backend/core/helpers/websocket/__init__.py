from core.fastapi.dependencies.permission.permissions import AllowAll
from core.helpers.websocket.manager import WebSocketConnectionManager


manager = WebSocketConnectionManager(AllowAll)

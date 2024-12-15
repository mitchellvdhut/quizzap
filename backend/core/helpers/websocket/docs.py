from core.helpers.websocket.schemas.docs import (
    RequestWebSocketDocsSchema,
    ResponseWebSocketDocsSchema,
    WebSocketDocsSchema,
    WebSocketPacketParams,
)
from core.enums.websocket import WebSocketActionEnum


actions = {}


actions[WebSocketActionEnum.STATUS_CODE] = WebSocketDocsSchema(
    info="Action for providing feedback.",
    response=ResponseWebSocketDocsSchema(info="Response with HTTP status code"),
)


actions[WebSocketActionEnum.POOL_MESSAGE] = WebSocketDocsSchema(
    info="Action for sending a message to the pool.",
    request=RequestWebSocketDocsSchema(
        info="Send a message to the pool",
        params=WebSocketPacketParams(payload={"message": "string"}),
    ),
    response=ResponseWebSocketDocsSchema(
        info="Receive a message from your pool.",
        params=WebSocketPacketParams(payload={"message": "string"}),
    ),
)


actions[WebSocketActionEnum.GLOBAL_MESSAGE] = WebSocketDocsSchema(
    info="Action for sending a message to all connections.",
    request=RequestWebSocketDocsSchema(
        info="Send a message to all connections",
        params=WebSocketPacketParams(payload={"message": "string"}),
    ),
    response=ResponseWebSocketDocsSchema(
        info="Receive a globally broadcasted message.",
        params=WebSocketPacketParams(payload={"message": "string"}),
    ),
)


actions[WebSocketActionEnum.USER_CONNECT] = WebSocketDocsSchema(
    info="Action for indicating a user has connected.",
    response=ResponseWebSocketDocsSchema(
        info="Receive the username of the newly connected user.",
        params=WebSocketPacketParams(payload={"username": "string"}),
    ),
)


actions[WebSocketActionEnum.USER_DISCONNECT] = WebSocketDocsSchema(
    info="Action for indicating a user has disconnected.",
    response=ResponseWebSocketDocsSchema(
        info="Receive the username of the disconnected user.",
        params=WebSocketPacketParams(payload={"username": "string"}),
    ),
)


actions[WebSocketActionEnum.SESSION_CLOSE] = WebSocketDocsSchema(
    info="Action for indicating the session has been irriversibly closed.",
    request=RequestWebSocketDocsSchema(
        info="Request termination of quiz session closage."
    ),
    response=ResponseWebSocketDocsSchema(
        info="Receive indication of session closage.",
        params=WebSocketPacketParams(payload={"message": "string"}),
    ),
)

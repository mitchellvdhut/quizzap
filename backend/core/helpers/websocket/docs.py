from core.helpers.websocket.schemas.docs import (
    RequestWebsocketDocsSchema,
    ResponseWebsocketDocsSchema,
    WebsocketDocsSchema,
    WebsocketPacketParams,
)
from core.enums.websocket import WebsocketActionEnum


actions = {}


actions[WebsocketActionEnum.STATUS_CODE] = WebsocketDocsSchema(
    info="Action for providing feedback.",
    response=ResponseWebsocketDocsSchema(info="Response with HTTP status code"),
)


actions[WebsocketActionEnum.POOL_MESSAGE] = WebsocketDocsSchema(
    info="Action for sending a message to the pool.",
    request=RequestWebsocketDocsSchema(
        info="Send a message to the pool",
        params=WebsocketPacketParams(payload={"message": "string"}),
    ),
    response=ResponseWebsocketDocsSchema(
        info="Receive a message from your pool.",
        params=WebsocketPacketParams(payload={"message": "string"}),
    ),
)


actions[WebsocketActionEnum.GLOBAL_MESSAGE] = WebsocketDocsSchema(
    info="Action for sending a message to all connections.",
    request=RequestWebsocketDocsSchema(
        info="Send a message to all connections",
        params=WebsocketPacketParams(payload={"message": "string"}),
    ),
    response=ResponseWebsocketDocsSchema(
        info="Receive a globally broadcasted message.",
        params=WebsocketPacketParams(payload={"message": "string"}),
    ),
)


actions[WebsocketActionEnum.USER_CONNECT] = WebsocketDocsSchema(
    info="Action for indicating a user has connected.",
    response=ResponseWebsocketDocsSchema(
        info="Receive the username of the newly connected user.",
        params=WebsocketPacketParams(payload={"username": "string"}),
    ),
)


actions[WebsocketActionEnum.USER_DISCONNECT] = WebsocketDocsSchema(
    info="Action for indicating a user has disconnected.",
    response=ResponseWebsocketDocsSchema(
        info="Receive the username of the disconnected user.",
        params=WebsocketPacketParams(payload={"username": "string"}),
    ),
)


actions[WebsocketActionEnum.SESSION_CLOSE] = WebsocketDocsSchema(
    info="Action for indicating the session has been irriversibly closed.",
    request=RequestWebsocketDocsSchema(
        info="Request termination of quiz session closage."
    ),
    response=ResponseWebsocketDocsSchema(
        info="Receive indication of session closage.",
        params=WebsocketPacketParams(payload={"message": "string"}),
    ),
)

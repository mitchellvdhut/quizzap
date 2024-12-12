import { WebsocketActions, type AnswerCount, type Message, type Question, type SessionId, type Username, type UserScore, type WebsocketConnection, type WebsocketPacket } from "@/types";

const baseUrl = import.meta.env.VITE_WEBSOCKET_URL + "/api/latest/sockets"

export function startWebsocket(url: string): WebsocketConnection {
  const ws = new WebSocket(baseUrl + url);

  const websocket: WebsocketConnection = {
    socket: ws,

    onDefault: (packet) => { console.error("Unhandled action", packet) },

    onStatusCode: (packet) => defaultFunction<typeof packet.payload>(packet),
    onPoolMessage: (packet) => defaultFunction<typeof packet.payload>(packet),
    onGlobalMessage: (packet) => defaultFunction<typeof packet.payload>(packet),
    onUserConnect: (packet) => defaultFunction<typeof packet.payload>(packet),
    onUserDisconnect: (packet) => defaultFunction<typeof packet.payload>(packet),
    onSessionClose: (packet) => defaultFunction<typeof packet.payload>(packet),
    onSessionCreated: (packet) => defaultFunction<typeof packet.payload>(packet),
    onQuestionInfo: (packet) => defaultFunction<typeof packet.payload>(packet),
    onQuestionStart: (packet) => defaultFunction<typeof packet.payload>(packet),
    onQuestionStop: (packet) => defaultFunction<typeof packet.payload>(packet),
    onScoreInfo: (packet) => defaultFunction<typeof packet.payload>(packet),
    onQuizEnd: (packet) => defaultFunction<typeof packet.payload>(packet),

    sendPoolMessage: (packet) => defaultSend<typeof packet.payload>(ws, packet),
    sendGlobalMessage: (packet) => defaultSend<typeof packet.payload>(ws, packet),
    sendCloseSession: (packet) => defaultSend<typeof packet.payload>(ws, packet),
    sendSubmitVote: (packet) => defaultSend<typeof packet.payload>(ws, packet),
    sendQuestionStart: (packet) => defaultSend<typeof packet.payload>(ws, packet),
    sendQuestionStop: (packet) => defaultSend<typeof packet.payload>(ws, packet),
  }

  ws.onmessage = (event) => {
    if (!event.data) {
      console.error("No data");
      return;
    }

    let data: WebsocketPacket<unknown> | null = null;

    try {
      data = JSON.parse(event.data);
    } catch (error) {
      console.log(event.data);
      console.log(error);
      return;
    }

    if (!data) {
      console.log("No data?");
      return;
    }

    switch (data.action) {
      case WebsocketActions.STATUS_CODE:
        websocket.onStatusCode(data as WebsocketPacket<null>);
        break;

      case WebsocketActions.POOL_MESSAGE:
        websocket.onPoolMessage(data as WebsocketPacket<Message>);
        break;

      case WebsocketActions.GLOBAL_MESSAGE:
        websocket.onGlobalMessage(data as WebsocketPacket<Message>);
        break;

      case WebsocketActions.USER_CONNECT:
        websocket.onUserConnect(data as WebsocketPacket<Username>);
        break;

      case WebsocketActions.USER_DISCONNECT:
        websocket.onUserDisconnect(data as WebsocketPacket<Username>);
        break;

      case WebsocketActions.SESSION_CLOSE:
        websocket.onSessionClose(data as WebsocketPacket<Message>);
        break;

      case WebsocketActions.SESSION_CREATED:
        websocket.onSessionCreated(data as WebsocketPacket<SessionId>);
        break;

      case WebsocketActions.QUESTION_INFO:
        websocket.onQuestionInfo(data as WebsocketPacket<Question>);
        break;

      case WebsocketActions.QUESTION_START:
        websocket.onQuestionStart(data as WebsocketPacket<AnswerCount>);
        break;

      case WebsocketActions.QUESTION_STOP:
        websocket.onQuestionStop(data as WebsocketPacket<null>);
        break;

      case WebsocketActions.SCORE_INFO:
        websocket.onScoreInfo(data as WebsocketPacket<UserScore[]>);
        break;

      default:
        websocket.onDefault(data);
        break;
    }
  }

  return websocket;
}

function defaultSend<T>(ws: WebSocket, packet: WebsocketPacket<T>) {
  const jsonData = JSON.stringify(packet);
  ws.send(jsonData);
}

function defaultFunction<T>(packet: WebsocketPacket<T>) {
  console.warn(`ACTION RESPONSE NOT IMPLEMENTED: ${packet.action}`, packet);
}

import {
  WebSocketActions,
  WebSocketState,
  WebSocketUserType,
  type AnswerCount,
  type HostWebSocketCallbacks,
  type HostWebSocketInteraction,
  type Message,
  type PlayerWebSocketCallbacks,
  type PlayerWebSocketInteraction,
  type Question,
  type ReceiveMessage,
  type SendWebSocketPacket,
  type SessionId, type Username,
  type UserScore, type Vote,
  type WebSocketConnection,
  type WebSocketInteraction,
  type WebSocketPacket,
  type WebSocketResult,
} from "@/types";

const baseUrl = import.meta.env.VITE_WEBSOCKET_URL + "/api/latest/sockets"

export function startWebSocket(url: string): WebSocketConnection {
  const ws = new WebSocket(baseUrl + url);

  const websocket: WebSocketConnection = {
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

    sendPoolMessage: () => { throw new Error("Function is not implemented") },
    sendCloseSession: () => { throw new Error("Function is not implemented") },
    sendSubmitVote: () => { throw new Error("Function is not implemented") },
    sendQuestionStart: () => { throw new Error("Function is not implemented") },
    sendQuestionStop: () => { throw new Error("Function is not implemented") },
  }

  websocket.sendPoolMessage = (payload) => {
    const packet: SendWebSocketPacket<Message> = {
      action: WebSocketActions.POOL_MESSAGE,
      message: "it's about sending a message",
      payload: payload,
    }

    defaultSend<Message>(websocket.socket, packet);
  };

  websocket.sendCloseSession = () => {
    const packet: SendWebSocketPacket = {
      action: WebSocketActions.SESSION_CLOSE,
      message: "closing session",
      payload: null,
    }

    defaultSend(websocket.socket, packet);
  };

  websocket.sendSubmitVote = (payload) => {
    const packet: SendWebSocketPacket<Vote> = {
      action: WebSocketActions.SUBMIT_VOTE,
      message: "submitting vote",
      payload: payload,
    }

    defaultSend<Vote>(websocket.socket, packet);
  };

  websocket.sendQuestionStart = () => {
    const packet: SendWebSocketPacket = {
      action: WebSocketActions.QUESTION_START,
      message: "requesting new question",
      payload: null,
    }

    defaultSend(websocket.socket, packet);
  };

  websocket.sendQuestionStop = () => {
    const packet: SendWebSocketPacket = {
      action: WebSocketActions.QUESTION_STOP,
      message: "stopping question",
      payload: null,
    }

    defaultSend(websocket.socket, packet);
  };

  function defaultSend<T>(ws: WebSocket, packet: SendWebSocketPacket<T>) {
    const jsonData = JSON.stringify(packet);
    ws.send(jsonData);
  }

  function defaultFunction<T>(packet: WebSocketPacket<T>) {
    console.warn(`ACTION RESPONSE NOT IMPLEMENTED: ${packet.action}`, packet);
  }

  ws.onmessage = (event) => {
    if (!event.data) {
      console.error("No data");
      return;
    }

    let data: WebSocketPacket<unknown> | null = null;

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
      case WebSocketActions.STATUS_CODE:
        websocket.onStatusCode(data as WebSocketPacket<null>);
        break;

      case WebSocketActions.POOL_MESSAGE:
        websocket.onPoolMessage(data as WebSocketPacket<ReceiveMessage>);
        break;

      case WebSocketActions.GLOBAL_MESSAGE:
        websocket.onGlobalMessage(data as WebSocketPacket<Message>);
        break;

      case WebSocketActions.USER_CONNECT:
        websocket.onUserConnect(data as WebSocketPacket<Username>);
        break;

      case WebSocketActions.USER_DISCONNECT:
        websocket.onUserDisconnect(data as WebSocketPacket<Username>);
        break;

      case WebSocketActions.SESSION_CLOSE:
        websocket.onSessionClose(data as WebSocketPacket<Message>);
        break;

      case WebSocketActions.SESSION_CREATED:
        websocket.onSessionCreated(data as WebSocketPacket<SessionId>);
        break;

      case WebSocketActions.QUESTION_INFO:
        websocket.onQuestionInfo(data as WebSocketPacket<Question>);
        break;

      case WebSocketActions.QUESTION_START:
        websocket.onQuestionStart(data as WebSocketPacket<AnswerCount>);
        break;

      case WebSocketActions.QUESTION_STOP:
        websocket.onQuestionStop(data as WebSocketPacket<null>);
        break;

      case WebSocketActions.SCORE_INFO:
        websocket.onScoreInfo(data as WebSocketPacket<UserScore[]>);
        break;

      default:
        websocket.onDefault(data);
        break;
    }
  }

  return websocket;
}

function getOrGenClientToken() {
  const storageKey = "clientToken";
  let clientToken = localStorage.getItem(storageKey);

  if (!clientToken) {
    clientToken = crypto.randomUUID();
    localStorage.setItem(storageKey, clientToken);
  }

  return clientToken;
}

export function createSession(quizId: string, callbacks: HostWebSocketCallbacks): WebSocketInteraction {
  const clientToken = getOrGenClientToken();
  const access_token = "insert access_token here";

  const url = `/quizCreate/${quizId}?access_token=${access_token}&client_token=${clientToken}`;
  const ws = startWebSocket(url);

  const interactable: HostWebSocketInteraction = {
    ws: ws,
    state: WebSocketState.QUIZ_READY,
    userType: WebSocketUserType.HOST,

    closeSession: () => { throw new Error("Function not implemented.") },
    startNextQuestion: () => { throw new Error("Function not implemented.") },
    stopQuestion: () => { throw new Error("Function not implemented.") },
    sendChat: () => { throw new Error("Function not implemented.") },
  }

  interactable.ws.onQuestionStop = () => {
    interactable.state = WebSocketState.IDLE;
    callbacks.onQuestionStop();
  }

  interactable.startNextQuestion = async (useCallback = true) => {
    interactable.ws.sendQuestionStart();

    const result = await generatePromise<Question>("onQuestionInfo");

    if (useCallback) {
      if (!result.ok) throw new Error(result.message);
      callbacks.onQuestionInfo(result.packet!.payload);
    }
    
    return result;
  }

  interactable.stopQuestion = async () => {
    interactable.ws.sendQuestionStop();

    return await generatePromise("onQuestionStop");
  }

  interactable.sendChat = async (message) => {
    interactable.ws.sendPoolMessage({ message: message });

    return await generatePromise("onPoolMessage");
  }

  async function generatePromise<T = null>(targetFunction: keyof WebSocketConnection, timeout?: number): Promise<WebSocketResult<T>> {
    return await _generatePromise<T>(interactable, targetFunction, timeout);
  }

  return interactable;
}

export function joinSession(sessionId: string, username: string, callbacks: PlayerWebSocketCallbacks) {
  const clientToken = getOrGenClientToken();

  const url = `/quizJoin/${sessionId}?username=${username}&client_token=${clientToken}`;
  const ws = startWebSocket(url);

  const interactable: PlayerWebSocketInteraction = {
    ws: ws,
    state: WebSocketState.QUIZ_READY,
    userType: WebSocketUserType.PLAYER,

    submitVote: () => { throw new Error("Function not implemented.") },
    sendChat: () => { throw new Error("Function not implemented.") },
  }

  interactable.ws.onQuestionStart = (packet) => {
    interactable.state = WebSocketState.QUESTION_ACTIVE;
    callbacks.onQuestionStart(packet.payload);
  }

  interactable.ws.onQuestionStop = () => {
    interactable.state = WebSocketState.IDLE;
    callbacks.onQuestionStop();
  }

  interactable.submitVote = (vote) => {
    interactable.ws.sendSubmitVote({ vote: vote });

    return generatePromise("onStatusCode");
  }

  interactable.sendChat = (message) => {
    interactable.ws.sendPoolMessage({ message: message });

    return generatePromise("onPoolMessage");
  }

  interactable.ws.onPoolMessage = (packet) => {
    interactable.state = WebSocketState.IDLE;
    callbacks.onChatMessage(packet.payload);
  }

  function generatePromise<T = null>(targetFunction: keyof WebSocketConnection, timeout?: number): Promise<WebSocketResult<T>> {
    return _generatePromise<T>(interactable, targetFunction, timeout);
  }

  return interactable;
}

function _generatePromise<T = null>(interactable: WebSocketInteraction, targetFunction: keyof WebSocketConnection, timeout: number = 5000): Promise<WebSocketResult<T>> {
  return new Promise((resolve, reject) => {
    const func = interactable.ws[targetFunction];

    if (!func) throw new Error("Function was not found on interactable");

    const timer = setTimeout(() => {
      const result: WebSocketResult = {
        ok: false,
        message: "timed out",
      };

      reject(result);

      // @ts-expect-error Function is 100% compatible, unless somehow the universe said no
      interactable.ws[targetFunction] = func;
    }, timeout);

    // @ts-expect-error Function is 100% compatible, unless somehow the universe said no
    interactable.ws[targetFunction] = (packet: WebSocketPacket<T>) => {
      const result: WebSocketResult<T> = {
        packet: packet,
        ok: packet.status_code == 200,
        message: "success",
      };

      resolve(result);

      clearTimeout(timer);

      // @ts-expect-error Function is 100% compatible, unless somehow the universe said no
      interactable.ws[targetFunction] = func;
    };
  });
}

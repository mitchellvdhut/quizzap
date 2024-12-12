import {
  WebsocketActions,
  WebsocketState,
  WebsocketUserType,
  type AnswerCount,
  type HostWebsocketCallbacks,
  type HostWebsocketInteraction,
  type Message,
  type PlayerWebsocketCallbacks,
  type PlayerWebsocketInteraction,
  type Question,
  type ReceiveMessage,
  type SendWebsocketPacket,
  type SessionId, type Username,
  type UserScore, type Vote,
  type WebsocketConnection,
  type WebsocketInteraction,
  type WebsocketPacket,
  type WebsocketResult,
} from "@/types";

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

    sendPoolMessage: () => { throw new Error("Function is not implemented") },
    sendCloseSession: () => { throw new Error("Function is not implemented") },
    sendSubmitVote: () => { throw new Error("Function is not implemented") },
    sendQuestionStart: () => { throw new Error("Function is not implemented") },
    sendQuestionStop: () => { throw new Error("Function is not implemented") },
  }

  websocket.sendPoolMessage = (payload) => {
    const packet: SendWebsocketPacket<Message> = {
      action: WebsocketActions.POOL_MESSAGE,
      message: "it's about sending a message",
      payload: payload,
    }

    defaultSend<Message>(websocket.socket, packet);
  };

  websocket.sendCloseSession = () => {
    const packet: SendWebsocketPacket = {
      action: WebsocketActions.SESSION_CLOSE,
      message: "closing session",
    }

    defaultSend(websocket.socket, packet);
  };

  websocket.sendSubmitVote = (payload) => {
    const packet: SendWebsocketPacket<Vote> = {
      action: WebsocketActions.SUBMIT_VOTE,
      message: "submitting vote",
      payload: payload,
    }

    defaultSend<Vote>(websocket.socket, packet);
  };

  websocket.sendQuestionStart = () => {
    const packet: SendWebsocketPacket = {
      action: WebsocketActions.QUESTION_START,
      message: "requesting new question",
    }

    defaultSend(websocket.socket, packet);
  };

  websocket.sendQuestionStop = () => {
    const packet: SendWebsocketPacket = {
      action: WebsocketActions.QUESTION_STOP,
      message: "stopping question",
    }

    defaultSend(websocket.socket, packet);
  };

  function defaultSend<T>(ws: WebSocket, packet: SendWebsocketPacket<T>) {
    const jsonData = JSON.stringify(packet);
    ws.send(jsonData);
  }

  function defaultFunction<T>(packet: WebsocketPacket<T>) {
    console.warn(`ACTION RESPONSE NOT IMPLEMENTED: ${packet.action}`, packet);
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
        websocket.onPoolMessage(data as WebsocketPacket<ReceiveMessage>);
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

function getOrGenClientToken() {
  const storageKey = "clientToken";
  let clientToken = localStorage.getItem(storageKey);

  if (!clientToken) {
    clientToken = crypto.randomUUID();
    localStorage.setItem(storageKey, clientToken);
  }

  return clientToken;
}

export function createSession(quizId: string, callbacks: HostWebsocketCallbacks): WebsocketInteraction {
  const clientToken = getOrGenClientToken();
  const access_token = "insert access_token here";

  const url = `/quizCreate/${quizId}?access_token=${access_token}&client_token=${clientToken}`;
  const ws = startWebsocket(url);

  const interactable: HostWebsocketInteraction = {
    ws: ws,
    state: WebsocketState.QUIZ_READY,
    userType: WebsocketUserType.HOST,

    closeSession: () => { throw new Error("Function not implemented.") },
    startNextQuestion: () => { throw new Error("Function not implemented.") },
    stopQuestion: () => { throw new Error("Function not implemented.") },
    sendChat: () => { throw new Error("Function not implemented.") },
  }

  interactable.ws.onQuestionStop = () => {
    interactable.state = WebsocketState.IDLE;
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

  async function generatePromise<T = null>(targetFunction: keyof WebsocketConnection, timeout?: number): Promise<WebsocketResult<T>> {
    return await _generatePromise<T>(interactable, targetFunction, timeout);
  }

  return interactable;
}

export function joinSession(sessionId: string, username: string, callbacks: PlayerWebsocketCallbacks) {
  const clientToken = getOrGenClientToken();

  const url = `/quizJoin/${sessionId}?username=${username}&client_token=${clientToken}`;
  const ws = startWebsocket(url);

  const interactable: PlayerWebsocketInteraction = {
    ws: ws,
    state: WebsocketState.QUIZ_READY,
    userType: WebsocketUserType.PLAYER,

    submitVote: () => { throw new Error("Function not implemented.") },
    sendChat: () => { throw new Error("Function not implemented.") },
  }

  interactable.ws.onQuestionStart = (packet) => {
    interactable.state = WebsocketState.QUESTION_ACTIVE;
    callbacks.onQuestionStart(packet.payload);
  }

  interactable.ws.onQuestionStop = () => {
    interactable.state = WebsocketState.IDLE;
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
    interactable.state = WebsocketState.IDLE;
    callbacks.onChatMessage(packet.payload);
  }

  function generatePromise<T = null>(targetFunction: keyof WebsocketConnection, timeout?: number): Promise<WebsocketResult<T>> {
    return _generatePromise<T>(interactable, targetFunction, timeout);
  }

  return interactable;
}

function _generatePromise<T = null>(interactable: WebsocketInteraction, targetFunction: keyof WebsocketConnection, timeout: number = 5000): Promise<WebsocketResult<T>> {
  return new Promise((resolve, reject) => {
    const func = interactable.ws[targetFunction];

    if (!func) throw new Error("Function was not found on interactable");

    const timer = setTimeout(() => {
      const result: WebsocketResult = {
        ok: false,
        message: "timed out",
      };

      reject(result);

      // @ts-expect-error Function is 100% compatible, unless somehow the universe said no
      interactable.ws[targetFunction] = func;
    }, timeout);

    // @ts-expect-error Function is 100% compatible, unless somehow the universe said no
    interactable.ws[targetFunction] = (packet: WebsocketPacket<T>) => {
      const result: WebsocketResult<T> = {
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

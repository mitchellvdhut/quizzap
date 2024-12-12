export interface Creator {
  username: string;
}

export interface Quiz {
  id: string,
  name: string,
  description: string,
  created_at: string,
  updated_at: string,
  creator: Creator,
  questions: Question[],
}

export interface Question {
  id?: number;
  question: string;
  answers: Answer[];
  answeringTimeInSeconds: number;
}

export interface Answer {
  id?: number;
  text: string;
  correct: boolean;
}

export enum WebsocketActions {
  STATUS_CODE = "STATUS_CODE",
  POOL_MESSAGE = "POOL_MESSAGE",
  GLOBAL_MESSAGE = "GLOBAL_MESSAGE",
  USER_CONNECT = "USER_CONNECT",
  USER_DISCONNECT = "USER_DISCONNECT",
  SESSION_CLOSE = "SESSION_CLOSE",
  SESSION_CREATED = "SESSION_CREATED",
  SUBMIT_VOTE = "SUBMIT_VOTE",
  QUESTION_INFO = "QUESTION_INFO",
  QUESTION_START = "QUESTION_START",
  QUESTION_STOP = "QUESTION_STOP",
  SCORE_INFO = "SCORE_INFO",
  QUIZ_END = "QUIZ_END",
}

export interface WebsocketPacket<T> {
  status_code: number;
  action: WebsocketActions;
  message: string;
  payload: T;
}

export interface Message {
  message: string;
}

export interface Username {
  username: string;
}

export interface SessionId {
  session_id: number;
}

export interface AnswerCount {
  answer_count: number;
}

export interface UserScore {
  username: string;
  score: number;
  streak: number;
}

export interface Vote {
  vote: number
}

export interface WebsocketConnection {
  socket: WebSocket;

  onDefault: (packet: WebsocketPacket<unknown>) => void;
  
  onStatusCode: (packet: WebsocketPacket<null>) => void;
  onPoolMessage: (packet: WebsocketPacket<Message>) => void;
  onGlobalMessage: (packet: WebsocketPacket<Message>) => void;
  onUserConnect: (packet: WebsocketPacket<Username>) => void;
  onUserDisconnect: (packet: WebsocketPacket<Username>) => void;
  onSessionClose: (packet: WebsocketPacket<Message>) => void;
  onSessionCreated: (packet: WebsocketPacket<SessionId>) => void;
  onQuestionInfo: (packet: WebsocketPacket<Question>) => void;
  onQuestionStart: (packet: WebsocketPacket<AnswerCount>) => void;
  onQuestionStop: (packet: WebsocketPacket<null>) => void;
  onScoreInfo: (packet: WebsocketPacket<UserScore[]>) => void;
  onQuizEnd: (packet: WebsocketPacket<null>) => void;

  sendPoolMessage: (packet: WebsocketPacket<Message>) => void;
  sendGlobalMessage: (packet: WebsocketPacket<Message>) => void;
  sendCloseSession: (packet: WebsocketPacket<null>) => void;
  sendSubmitVote: (packet: WebsocketPacket<Vote>) => void;
  sendQuestionStart: (packet: WebsocketPacket<null>) => void;
  sendQuestionStop: (packet: WebsocketPacket<null>) => void;
}

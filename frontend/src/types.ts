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
  id: string;
  name: string;
  description: string;
  time_limit: number; // in seconds
  answers: Answer[];
}

export interface Answer {
  id: string;
  description: string;
  is_correct: boolean;
}

export interface AnswerInfo {
  answer_count: number;
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

export interface SendWebsocketPacket<T = null> {
  action: WebsocketActions;
  message: string;
  payload?: T;
}

export interface WebsocketPacket<T = null> {
  status_code: number;
  action: WebsocketActions;
  message: string;
  payload: T;
}

export interface Message {
  message: string;
}

export interface ReceiveMessage {
  username: string;
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
  onPoolMessage: (packet: WebsocketPacket<ReceiveMessage>) => void;
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

  sendPoolMessage: (payload: Message) => void;
  sendCloseSession: () => void;
  sendSubmitVote: (payload: Vote) => void;
  sendQuestionStart: () => void;
  sendQuestionStop: () => void;
}

export enum WebsocketState {
  QUIZ_READY = "QUIZ_READY",
  QUESTION_ACTIVE = "QUESTION_ACTIVE",
  IDLE = "IDLE",
  QUIZ_ENDED = "QUIZ_ENDED",
  LOADING = "LOADING",
}

export enum WebsocketUserType {
  HOST = "HOST",
  PLAYER = "PLAYER",
}

export interface WebsocketResult<T = null> {
  packet?: WebsocketPacket<T>;
  ok: boolean;
  message: string;
}

export interface WebsocketInteraction {
  ws: WebsocketConnection;
  state: WebsocketState;
  userType: WebsocketUserType;
}

export interface HostWebsocketInteraction extends WebsocketInteraction {
  closeSession: () => Promise<WebsocketResult>;
  startNextQuestion: (useCallback: boolean) => Promise<WebsocketResult<Question>>; // returns null if useCallback is true
  stopQuestion: () => Promise<WebsocketResult>;
  sendChat: (message: string) => Promise<WebsocketResult<Message>>;
}

export interface HostWebsocketCallbacks {
  onQuestionStop: () => void;
  onChatMessage: (username: string, message: string) => void;
  onQuestionInfo: (question: Question) => void;
}

export interface PlayerWebsocketInteraction extends WebsocketInteraction {
  submitVote: (vote: number) => Promise<WebsocketResult>;
  sendChat: (message: string) => Promise<WebsocketResult<Message>>;
}

export interface PlayerWebsocketCallbacks {
  onQuestionStart: (answerInfo: AnswerInfo) => void;
  onQuestionStop: () => void;
  onChatMessage: (message: ReceiveMessage) => void;
}

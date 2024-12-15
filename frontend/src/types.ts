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

export enum WebSocketActions {
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

export interface SendWebSocketPacket<T = null> {
  action: WebSocketActions;
  message: string;
  payload: T;
}

export interface WebSocketPacket<T = null> {
  status_code: number;
  action: WebSocketActions;
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

export interface WebSocketConnection {
  socket: WebSocket;

  onDefault: (packet: WebSocketPacket<unknown>) => void;
  
  onStatusCode: (packet: WebSocketPacket<null>) => void;
  onPoolMessage: (packet: WebSocketPacket<ReceiveMessage>) => void;
  onGlobalMessage: (packet: WebSocketPacket<Message>) => void;
  onUserConnect: (packet: WebSocketPacket<Username>) => void;
  onUserDisconnect: (packet: WebSocketPacket<Username>) => void;
  onSessionClose: (packet: WebSocketPacket<Message>) => void;
  onSessionCreated: (packet: WebSocketPacket<SessionId>) => void;
  onQuestionInfo: (packet: WebSocketPacket<Question>) => void;
  onQuestionStart: (packet: WebSocketPacket<AnswerCount>) => void;
  onQuestionStop: (packet: WebSocketPacket<null>) => void;
  onScoreInfo: (packet: WebSocketPacket<UserScore[]>) => void;
  onQuizEnd: (packet: WebSocketPacket<null>) => void;

  sendPoolMessage: (payload: Message) => void;
  sendCloseSession: () => void;
  sendSubmitVote: (payload: Vote) => void;
  sendQuestionStart: () => void;
  sendQuestionStop: () => void;
}

export enum WebSocketState {
  QUIZ_READY = "QUIZ_READY",
  QUESTION_ACTIVE = "QUESTION_ACTIVE",
  IDLE = "IDLE",
  QUIZ_ENDED = "QUIZ_ENDED",
  LOADING = "LOADING",
}

export enum WebSocketUserType {
  HOST = "HOST",
  PLAYER = "PLAYER",
}

export interface WebSocketResult<T = null> {
  packet?: WebSocketPacket<T>;
  ok: boolean;
  message: string;
}

export interface WebSocketInteraction {
  ws: WebSocketConnection;
  state: WebSocketState;
  userType: WebSocketUserType;
}

export interface HostWebSocketInteraction extends WebSocketInteraction {
  closeSession: () => Promise<WebSocketResult>;
  startNextQuestion: (useCallback: boolean) => Promise<WebSocketResult<Question>>; // returns null if useCallback is true
  stopQuestion: () => Promise<WebSocketResult>;
  sendChat: (message: string) => Promise<WebSocketResult<Message>>;
}

export interface HostWebSocketCallbacks {
  onQuestionStop: () => void;
  onChatMessage: (username: string, message: string) => void;
  onQuestionInfo: (question: Question) => void;
}

export interface PlayerWebSocketInteraction extends WebSocketInteraction {
  submitVote: (vote: number) => Promise<WebSocketResult>;
  sendChat: (message: string) => Promise<WebSocketResult<Message>>;
}

export interface PlayerWebSocketCallbacks {
  onQuestionStart: (answerInfo: AnswerInfo) => void;
  onQuestionStop: () => void;
  onChatMessage: (message: ReceiveMessage) => void;
}

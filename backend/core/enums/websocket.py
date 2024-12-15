from enum import Enum


class WebSocketActionEnum(str, Enum):
    STATUS_CODE = "STATUS_CODE"         # Send a HTTP like status code
    POOL_MESSAGE = "POOL_MESSAGE"       # Send a simple message to all in pool
    GLOBAL_MESSAGE = "GLOBAL_MESSAGE"   # Send a simple message to all connected
    USER_CONNECT = "USER_CONNECT"       # New user has connected
    USER_DISCONNECT = "USER_DISCONNECT" # User has disconnected
    SESSION_CLOSE = "SESSION_CLOSE"     # Session is closing


class WebSocketSessionEnum(str, Enum):
    READY = "READY"             # Ready for starting internal session
    STARTING = "STARTING"       # Starting internal session
    STARTED = "STARTED"         # Started internal session, ready for connections
    IN_PROGRESS = "IN_PROGRESS" # Session is in progress of task (task is for the client)
    FINISHED = "FINISHED"       # Session is has finished task (task is for the client)
    STOPPING = "STOPPING"       # Internal session is stopping
    STOPPED = "STOPPED"         # Internal session has stopped


class WebSocketTargetEnum(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    POOL = "POOL"
    GLOBAL = "GLOBAL"


class QuizSessionActionEnum(str, Enum):
    # When editing this, edit .\app\quiz\websocket\docs.py too
    SESSION_CREATED = "SESSION_CREATED"  # Respond with a new session ID 
    SUBMIT_VOTE = "SUBMIT_VOTE"          # Send an answer vote to the session
    QUESTION_INFO = "QUESTION_INFO"      # Sends question info
    QUESTION_START = "QUESTION_START"    # Notify next question
    QUESTION_STOP = "QUESTION_STOP"      # Notify no question
    SCORE_INFO = "SCORE_INFO"            # Responds with all player scores
    QUIZ_END = "QUIZ_END"                # Indicate the end of the quiz
    USER_RECONNECT = "USER_RECONNECT"    # Indicate user reconnect
    KICK_USER = "KICK_USER"              # Kick a user from session


class QuizStateEnum(str, Enum):
    READY = "READY"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"

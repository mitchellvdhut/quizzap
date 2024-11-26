from enum import Enum


class BaseEnum(Enum):
    pass


class UserEnum(BaseEnum):
    pass


class WebsocketActionEnum(str, BaseEnum):
    STATUS_CODE = "STATUS_CODE"         # Send a HTTP like status code
    POOL_MESSAGE = "POOL_MESSAGE"       # Send a simple message to all in pool
    GLOBAL_MESSAGE = "GLOBAL_MESSAGE"   # Send a simple message to all connected
    USER_CONNECT = "USER_CONNECT"       # New user has connected
    USER_DISCONNECT = "USER_DISCONNECT" # User has disconnected
    SESSION_CLOSE = "SESSION_CLOSE"     # Session is closing


class WebsocketSessionEnum(str, BaseEnum):
    READY = "READY"             # Ready for starting internal session
    STARTING = "STARTING"       # Starting internal session
    STARTED = "STARTED"         # Started internal session, ready for connections
    IN_PROGRESS = "IN_PROGRESS" # Session is in progress of task (task is for the client)
    FINISHED = "FINISHED"       # Session is has finished task (task is for the client)
    STOPPING = "STOPPING"       # Internal session is stopping
    STOPPED = "STOPPED"         # Internal session has stopped


class QuizSessionActionEnum(str, BaseEnum):
    # When editing this, edit app\swipe_session\services\action_docs.py too
    SUBMIT_VOTE = "SUBMIT_VOTE"       # Send an answer vote to the session 
    QUESTION_START = "QUESTION_START" # Notify next question
    QUESTION_STOP = "QUESTION_STOP"   # Notify no question

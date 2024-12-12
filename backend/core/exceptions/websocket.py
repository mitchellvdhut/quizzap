from core.exceptions.base import CustomException


class ConnectionCode:
    status_code = 200
    message = "connection status_code"

    def __init__(self, status_code, message) -> None:
        self.status_code = status_code
        self.message = message


class SuccessfullConnection(ConnectionCode):
    status_code = 202
    message = "you have connected"


class RequestSuccessful(ConnectionCode):
    status_code = 200
    message = "request has been handled successfully"


class ClosingConnection(ConnectionCode):
    status_code = 200
    message = "you have been forcefully disconnected"


class InactiveException(CustomException):
    status_code = 400
    error_status_code = "WEBSOCKET__INACTIVE_SESSION"
    message = "you cannot connect to an inactive session"


class NoMessageException(CustomException):
    status_code = 400
    error_status_code = "WEBSOCKET__NO_MESSAGE"
    message = "no message provided"


class JSONSerializableException(CustomException):
    status_code = 400
    error_status_code = "WEBSOCKET__JSON_UNSERIALIZABLE"
    message = "data is not JSON serializable"


class ValidationException(CustomException):
    status_code = 400
    error_status_code = "WEBSOCKET__VALIDATION_ERROR"
    message = "pydantic schema validation failed"


class InvalidIdException(CustomException):
    status_code = 400
    error_status_code = "WEBSOCKET__INVALID_ID"
    message = "either session or user id is invalid"


class QuizStoppedException(CustomException):
    status_code = 400
    error_status_code = "WEBSOCKET__QUIZ_STOPPED"
    message = "quiz has already stopped"


class InvalidVoteException(CustomException):
    status_code = 400
    error_status_code = "WEBSOCKET__INVALID_VOTE"
    message = "vote index is out of range"


class NoQuestionException(CustomException):
    status_code = 400
    error_status_code = "WEBSOCKET__NO_QUESTION"
    message = "there is no question currently active"


class AlreadyVotedException(CustomException):
    status_code = 409
    error_status_code = "WEBSOCKET__ALREADY_VOTED"
    message = "you have already voted on this question"


class AccessDeniedException(CustomException):
    status_code = 403
    error_status_code = "WEBSOCKET__ACCESS_DENIED"
    message = "access denied"


class StatusNotFoundException(CustomException):
    status_code = 404
    error_status_code = "WEBSOCKET__STATUS_NOT_FOUND"
    message = "status does not exist"


class SessionNotFoundException(CustomException):
    status_code = 404
    error_status_code = "WEBSOCKET__SESSION_NOT_FOUND"
    message = "session does not exist"


class ActionNotFoundException(CustomException):
    status_code = 404
    error_status_code = "WEBSOCKET__ACTION_NOT_FOUND"
    message = "action does not exist"


class AlreadySwipedException(CustomException):
    status_code = 409
    error_status_code = "WEBSOCKET__SWIPE_CONFLICT"
    message = "this user has already swiped this recipe in this session"


class ActionNotImplementedException(CustomException):
    status_code = 501
    error_status_code = "WEBSOCKET__ACTION_NOT_IMPLEMENTED"
    message = "action is not implemented or not available"

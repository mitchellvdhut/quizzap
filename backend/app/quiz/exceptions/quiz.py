from core.exceptions.base import CustomException


class DuplicateNameException(CustomException):
    status_code = 409
    error_code = "QUIZ__DUPLICATE_NAME"
    message = "duplicate quiz name"


class QuizNotFoundException(CustomException):
    status_code = 404
    error_code = "QUIZ__NOT_FOUND"
    message = "quiz not found"

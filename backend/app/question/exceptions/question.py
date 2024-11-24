from core.exceptions.base import CustomException


class DuplicateNameException(CustomException):
    status_code = 409
    error_code = "QUESTION__DUPLICATE_NAME"
    message = "duplicate question name"


class QuestionNotFoundException(CustomException):
    status_code = 404
    error_code = "QUESTION__NOT_FOUND"
    message = "question not found"

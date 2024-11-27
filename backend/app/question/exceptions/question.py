from core.exceptions.base import CustomException


class QuestionNotFoundException(CustomException):
    status_code = 404
    error_code = "QUESTION__NOT_FOUND"
    message = "question not found"

from core.exceptions.base import CustomException


class AnswerNotFoundException(CustomException):
    status_code = 404
    error_code = "ANSWER__NOT_FOUND"
    message = "answer not found"

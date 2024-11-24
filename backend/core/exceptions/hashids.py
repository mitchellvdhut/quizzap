from .base import CustomException


class IncorrectHashIDException(CustomException):
    status_code = 400
    error_code = "HASH__INCORRECT_HASH_ID"
    message = "the inputted hash was incorrect"

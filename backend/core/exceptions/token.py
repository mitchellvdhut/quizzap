from core.exceptions.base import CustomException


class DecodeTokenException(CustomException):
    status_code = 400
    error_code = "TOKEN__DECODE_ERROR"
    message = "token decode error"


class ExpiredTokenException(CustomException):
    status_code = 400
    error_code = "TOKEN__EXPIRE_TOKEN"
    message = "expired token"

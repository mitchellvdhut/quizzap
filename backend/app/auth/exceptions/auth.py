from core.exceptions.base import CustomException


class BadCredentialsException(CustomException):
    status_code = 401
    error_code = "AUTH__BAD_CREDENTIALS"
    message = "credentials were incorrect"

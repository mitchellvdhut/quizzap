from core.exceptions.base import CustomException


class DuplicateUsernameException(CustomException):
    status_code = 409
    error_code = "USER__DUPLICATE_USERNAME"
    message = "duplicate username"


class UserNotFoundException(CustomException):
    status_code = 404
    error_code = "USER__NOT_FOUND"
    message = "user not found"

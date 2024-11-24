from http import HTTPStatus


class CustomException(Exception):
    status_code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message

    def __str__(self) -> str:
        return str(self.error_code)


class BadRequestException(CustomException):
    status_code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description


class NotFoundException(CustomException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description


class ForbiddenException(CustomException):
    status_code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = HTTPStatus.FORBIDDEN.description


class UnauthorizedException(CustomException):
    status_code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    message = HTTPStatus.UNAUTHORIZED.description


class UnprocessableEntity(CustomException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description

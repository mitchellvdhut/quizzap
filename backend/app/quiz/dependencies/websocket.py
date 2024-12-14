import logging
from typing import Annotated
from fastapi import Cookie, Query, WebSocketException, status


async def get_cookie_or_token(
    access_token: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    """Retrieve access_token from cookie or query parameter"""
    if access_token is None and token is None:
        logger = logging.getLogger("quizzap")
        logger.error("No cookie or token provided.")
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return access_token or token

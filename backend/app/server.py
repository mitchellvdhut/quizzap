"""
Initialize app
"""

from fastapi import FastAPI, Depends, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api import router
from core.config import config
from core.exceptions.base import CustomException
from core.fastapi.dependencies.logging import Logging
from core.fastapi.middlewares import (
    AuthenticationMiddleware,
    AuthBackend,
    # ResponseLogMiddleware,
)
from core.versioning import VersionedFastAPI


def init_routers(app_: FastAPI) -> None:
    """
    Initialize app routers
    """
    app_.include_router(router)


def init_listeners(app_: FastAPI) -> None:
    """
    Initialize app listeners
    """

    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        del request

        return JSONResponse(
            status_code=exc.status_code,
            content={"error_code": exc.error_code, "message": exc.message},
        )

    @app_.exception_handler(Exception)
    async def unicorn_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "Exception": f"{exc.__class__.__name__}{exc.args}",
                "message": "This is not pretty is it..?",
            },
        )


def on_auth_error(exc: Exception):
    """
    Authentication exception handler
    """
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> list[Middleware]:
    """
    Initialize FastAPI middleware
    """
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        # Middleware(ResponseLogMiddleware),
    ]
    return middleware


def create_app() -> FastAPI:
    """
    Create app
    """
    app_ = FastAPI(
        title=config.TITLE,
        description=config.DESC,
        version="0.0.1",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )

    init_routers(app_=app_)
    init_listeners(app_=app_)

    app_ = VersionedFastAPI(
        app_,
        init_func=init_listeners,
        enable_latest=True,
        version_format="{major}",
        prefix_format="/v{major}",
        app_prefix="/api",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )

    return app_


app = create_app()


# Greg is disappointed

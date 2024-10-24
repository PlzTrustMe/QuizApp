from fastapi import FastAPI

from .exceptions import setup_exception_handlers
from .healthcheck import healthcheck_router
from .user import user_router


def setup_routers(app: FastAPI) -> None:
    app.include_router(healthcheck_router)
    app.include_router(user_router)
    setup_exception_handlers(app)

from fastapi import FastAPI

from .company import company_router
from .exceptions import setup_exception_handlers
from .healthcheck import healthcheck_router
from .invite import invite_router
from .notification import notification_router
from .quiz import quiz_router
from .user import user_router


def setup_routers(app: FastAPI) -> None:
    app.include_router(healthcheck_router)
    app.include_router(user_router)
    app.include_router(company_router)
    app.include_router(invite_router)
    app.include_router(quiz_router)
    app.include_router(notification_router)
    setup_exception_handlers(app)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .healthcheck import healthcheck_router


def setup_routers(app: FastAPI) -> None:
    app.include_router(healthcheck_router)


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

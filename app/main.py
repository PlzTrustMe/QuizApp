import logging
from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import load_config
from app.infrastructure.bootstrap.di import setup_http_di
from app.infrastructure.persistence.models import map_tables
from app.routers import setup_routers

logger = logging.getLogger(__name__)


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    logger.debug("Initialize API")

    app = FastAPI(
        title="Quiz app",
        docs_url="/api/docs",
        description="Application for internship at meduzzen",
        debug=True,
        lifespan=lifespan,
    )

    setup_routers(app)
    setup_middlewares(app)

    setup_dishka(setup_http_di(), app)

    map_tables()

    return app


if __name__ == "__main__":
    config = load_config()

    uvicorn.run(
        "app.main:create_app",
        host=config.web_config.server_host,
        port=config.web_config.server_port,
        log_level=logging.INFO,
        reload=True,
        factory=True,
        lifespan="on",
    )

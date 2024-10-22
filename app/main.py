import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import load_config
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


def create_app() -> FastAPI:
    logger.debug("Initialize API")

    app = FastAPI(
        title="Quiz app",
        docs_url="/api/docs",
        description="Application for internship at meduzzen",
        debug=True
    )

    setup_routers(app)
    setup_middlewares(app)

    return app


if __name__ == "__main__":
    config = load_config()

    uvicorn.run(
        "app.main:create_app",
        host=config.web_config.server_host,
        port=config.web_config.server_port,
        log_level=logging.INFO,
        reload=True,
        factory=True
    )

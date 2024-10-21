import logging

import uvicorn
from fastapi import FastAPI

from app.config import load_config
from app.routers import setup_middlewares, setup_routers

logger = logging.getLogger(__name__)


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
        "main:create_app",
        host=config.web_config.server_host,
        port=config.web_config.server_port,
        reload=True,
        log_level=logging.INFO,
        factory=True
    )

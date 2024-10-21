import asyncio
import logging

import uvicorn
from fastapi import FastAPI

from app.routers.setup import setup_routers

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

    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        reload=True,
        log_level=logging.INFO,
        factory=True
    )

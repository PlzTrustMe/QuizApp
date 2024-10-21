import logging

from fastapi import FastAPI

from app.routers import setup_routers

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

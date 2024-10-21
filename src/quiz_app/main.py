import asyncio
import logging

import uvicorn
from fastapi import FastAPI

from quiz_app.routers.setup import setup_routers

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


async def run_api(app: FastAPI) -> None:
    config = uvicorn.Config(app, reload=True, log_level=logging.INFO)
    server = uvicorn.Server(config)

    logger.info("Running API")
    await server.serve()


async def main() -> None:
    logger.info("Launch app")

    app = create_app()
    await run_api(app)


if __name__ == "__main__":
    asyncio.run(main())

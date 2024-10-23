import logging
from typing import AsyncGenerator

from redis.asyncio import Redis

from app.infrastructure.cache.config import RedisConfig


async def get_redis(config: RedisConfig) -> AsyncGenerator[Redis, None]:
    redis = Redis.from_url(
        url=config.get_connection_url(),
        encoding="utf-8",
        decode_responses=True,
    )

    logging.info("Redis client was created.")

    try:
        yield redis
    finally:
        await redis.close()
        logging.info("Redis client has been closed.")

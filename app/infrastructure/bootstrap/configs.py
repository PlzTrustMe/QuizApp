import logging
from dataclasses import dataclass

from environs import Env

from app.infrastructure.cache.config import RedisConfig
from app.infrastructure.persistence.config import DBConfig


@dataclass
class AllConfigs:
    db: DBConfig
    cache: RedisConfig


def load_all_configs() -> AllConfigs:
    env = Env()
    env.read_env(".env")

    db_config = DBConfig(
        user=env.str("POSTGRES_USER"),
        password=env.str("POSTGRES_PASSWORD"),
        host=env.str("POSTGRES_HOST"),
        port=env.int("POSTGRES_PORT"),
        db_name=env.str("POSTGRES_DB"),
    )

    cache_config = RedisConfig(
        password=env.str("REDIS_PASSWORD"),
        host=env.str("REDIS_HOST"),
        port=env.int("REDIS_PORT"),
        db=env.int("REDIS_DB"),
    )

    logging.info("All configs loaded.")

    return AllConfigs(db=db_config, cache=cache_config)

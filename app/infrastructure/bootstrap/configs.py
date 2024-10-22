import logging
from dataclasses import dataclass

from environs import Env

from app.infrastructure.persistence.config import DBConfig


@dataclass
class AllConfigs:
    db: DBConfig


def load_all_configs() -> AllConfigs:
    env = Env()
    env.read_env(".env")

    db_config = DBConfig(
        user=env.str("POSTGRES_USER"),
        password=env.str("POSTGRES_PASSWORD"),
        host=env.str("POSTGRES_HOST"),
        port=env.int("POSTGRES_PORT"),
        db_name=env.str("POSTGRES_DB")
    )

    logging.info("All configs loaded.")

    return AllConfigs(
        db=db_config
    )

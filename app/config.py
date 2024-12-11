import logging
from dataclasses import dataclass

from environs import Env

logger = logging.getLogger(__name__)


@dataclass
class WebConfig:
    server_host: str
    server_port: int

    @staticmethod
    def from_env(env: Env) -> "WebConfig":
        server_host = env.str("SERVER_HOST")
        server_port = env.int("SERVER_PORT")

        return WebConfig(server_host=server_host, server_port=server_port)


@dataclass
class Config:
    web_config: WebConfig


def load_config() -> Config:
    env = Env()
    env.read_env(".env")

    config = Config(web_config=WebConfig.from_env(env))

    logger.info("Config successfully loaded")

    return config

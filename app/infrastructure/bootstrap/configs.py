import logging
from dataclasses import dataclass

from environs import Env

from app.infrastructure.cache.config import RedisConfig
from app.infrastructure.jwt.config import Auth0Config, JWTConfig
from app.infrastructure.persistence.config import DBConfig
from app.routers.auth.config import TokenAuthConfig


@dataclass
class AllConfigs:
    db: DBConfig
    cache: RedisConfig
    jwt: JWTConfig
    auth0: Auth0Config
    token_auth: TokenAuthConfig


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

    jwt_config = JWTConfig(
        key=env.str("JWT_KEY"), algorithm=env.str("JWT_ALGORITHM")
    )

    auth0_config = Auth0Config(
        domain=env.str("DOMAIN"), audience=env.str("AUDIENCE")
    )

    token_auth_config = TokenAuthConfig(token_cookies_key=jwt_config.key)

    logging.info("All configs loaded.")

    return AllConfigs(
        db=db_config,
        cache=cache_config,
        jwt=jwt_config,
        token_auth=token_auth_config,
        auth0=auth0_config,
    )

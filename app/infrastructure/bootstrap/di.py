from typing import Iterable

from dishka import AsyncContainer, Provider, Scope, make_async_container

from app.infrastructure.bootstrap.configs import load_all_configs
from app.infrastructure.cache.config import RedisConfig
from app.infrastructure.cache.provider import get_redis
from app.infrastructure.persistence.config import DBConfig
from app.infrastructure.persistence.provider import (
    get_async_session, get_async_sessionmaker,
    get_engine
)


def db_provider() -> Provider:
    provider = Provider()

    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_async_sessionmaker, scope=Scope.APP)
    provider.provide(get_async_session, scope=Scope.REQUEST)

    return provider


def cache_provider() -> Provider:
    provider = Provider()

    provider.provide(get_redis, scope=Scope.APP)

    return provider


def config_provider() -> Provider:
    provider = Provider()

    config = load_all_configs()

    provider.provide(lambda: config.db, scope=Scope.APP, provides=DBConfig)
    provider.provide(
        lambda: config.cache,
        scope=Scope.APP,
        provides=RedisConfig
    )

    return provider


def setup_providers() -> Iterable[Provider]:
    return [
        db_provider(),
        cache_provider(),
        config_provider()
    ]


def setup_http_di() -> AsyncContainer:
    providers = setup_providers()

    container = make_async_container(*providers)

    return container

from typing import Iterable

import argon2
from dishka import AsyncContainer, Provider, Scope, make_async_container

from app.core.commands.delete_user import DeleteUser
from app.core.commands.edit_full_name import EditFullName
from app.core.commands.sign_up import SignUp
from app.core.common.commiter import Commiter
from app.core.interfaces.password_hasher import PasswordHasher
from app.core.interfaces.user_gateways import UserGateway, UserReader
from app.core.queries.get_user import GetUserById
from app.core.queries.get_users import GetUsers
from app.infrastructure.auth.password_hasher import ArgonPasswordHasher
from app.infrastructure.bootstrap.configs import load_all_configs
from app.infrastructure.cache.config import RedisConfig
from app.infrastructure.cache.provider import get_redis
from app.infrastructure.persistence.commiter import SACommiter
from app.infrastructure.persistence.config import DBConfig
from app.infrastructure.persistence.gateways.user import (
    SQLAlchemyUserReader,
    UserMapper,
)
from app.infrastructure.persistence.provider import (
    get_async_session,
    get_async_sessionmaker,
    get_engine,
)


def gateway_provider() -> Provider:
    provider = Provider()

    provider.provide(UserMapper, scope=Scope.REQUEST, provides=UserGateway)
    provider.provide(
        SQLAlchemyUserReader, scope=Scope.REQUEST, provides=UserReader
    )

    provider.provide(
        SACommiter,
        scope=Scope.REQUEST,
        provides=Commiter,
    )
    return provider


def db_provider() -> Provider:
    provider = Provider()

    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_async_sessionmaker, scope=Scope.APP)
    provider.provide(get_async_session, scope=Scope.REQUEST)

    return provider


def interactor_provider() -> Provider:
    provider = Provider()

    provider.provide(SignUp, scope=Scope.REQUEST)
    provider.provide(EditFullName, scope=Scope.REQUEST)
    provider.provide(DeleteUser, scope=Scope.REQUEST)
    provider.provide(GetUserById, scope=Scope.REQUEST)
    provider.provide(GetUsers, scope=Scope.REQUEST)

    return provider


def cache_provider() -> Provider:
    provider = Provider()

    provider.provide(get_redis, scope=Scope.APP)

    return provider


def service_provider() -> Provider:
    provider = Provider()

    provider.provide(
        lambda: ArgonPasswordHasher(argon2.PasswordHasher()),
        scope=Scope.APP,
        provides=PasswordHasher,
    )

    return provider


def config_provider() -> Provider:
    provider = Provider()

    config = load_all_configs()

    provider.provide(lambda: config.db, scope=Scope.APP, provides=DBConfig)
    provider.provide(
        lambda: config.cache, scope=Scope.APP, provides=RedisConfig
    )

    return provider


def setup_providers() -> Iterable[Provider]:
    return [
        gateway_provider(),
        db_provider(),
        interactor_provider(),
        cache_provider(),
        config_provider(),
        service_provider(),
    ]


def setup_http_di() -> AsyncContainer:
    providers = setup_providers()

    container = make_async_container(*providers)

    return container

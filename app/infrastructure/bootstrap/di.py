from typing import Iterable

import argon2
from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from fastapi import Request

from app.core.commands.delete_user import DeleteUser
from app.core.commands.edit_full_name import EditFullName
from app.core.commands.sign_in import AccessTokenData, SignIn
from app.core.commands.sign_in_by_oauth import SignInByOauth
from app.core.commands.sign_up import SignUp
from app.core.common.commiter import Commiter
from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.password_hasher import PasswordHasher
from app.core.interfaces.user_gateways import UserGateway, UserReader
from app.core.queries.get_me import GetMe
from app.core.queries.get_user import GetUserById
from app.core.queries.get_users import GetUsers
from app.infrastructure.auth.access_token_processor import AccessTokenProcessor
from app.infrastructure.auth.id_provider import TokenIdProvider
from app.infrastructure.auth.password_hasher import ArgonPasswordHasher
from app.infrastructure.bootstrap.configs import load_all_configs
from app.infrastructure.cache.config import RedisConfig
from app.infrastructure.cache.provider import get_redis
from app.infrastructure.jwt.config import Auth0Config, JWTConfig
from app.infrastructure.jwt.jwt_processor import JWTProcessor, PyJWTProcessor
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
from app.routers.auth.config import TokenAuthConfig
from app.routers.auth.token_auth import TokenAuth


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
    provider.provide(SignIn, scope=Scope.REQUEST)
    provider.provide(SignInByOauth, scope=Scope.REQUEST)
    provider.provide(GetMe, scope=Scope.REQUEST)
    provider.provide(EditFullName, scope=Scope.REQUEST)
    provider.provide(DeleteUser, scope=Scope.REQUEST)
    provider.provide(GetUserById, scope=Scope.REQUEST)
    provider.provide(GetUsers, scope=Scope.REQUEST)

    return provider


def cache_provider() -> Provider:
    provider = Provider()

    provider.provide(get_redis, scope=Scope.APP)

    return provider


def infrastructure_provider() -> Provider:
    provider = Provider()

    provider.provide(PyJWTProcessor, scope=Scope.APP, provides=JWTProcessor)
    provider.provide(AccessTokenProcessor, scope=Scope.APP)

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
    provider.provide(lambda: config.jwt, scope=Scope.APP, provides=JWTConfig)
    provider.provide(
        lambda: config.token_auth, scope=Scope.APP, provides=TokenAuthConfig
    )
    provider.provide(
        lambda: config.auth0, scope=Scope.APP, provides=Auth0Config
    )

    return provider


class HTTPProvider(Provider):
    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def get_token_auth(
        self,
        request: Request,
        token_processor: AccessTokenProcessor,
        token_auth_config: TokenAuthConfig,
    ) -> TokenAuth:
        token_auth = TokenAuth(
            request=request,
            token_processor=token_processor,
            config=token_auth_config,
        )
        return token_auth

    @provide(scope=Scope.REQUEST)
    def get_access_token(self, token_auth: TokenAuth) -> AccessTokenData:
        token = token_auth.get_access_token()
        return token

    @provide(scope=Scope.REQUEST)
    def get_idp(
        self, token_auth: TokenAuth, user_reader: UserReader
    ) -> IdProvider:
        token = token_auth.get_access_token()
        id_provider = TokenIdProvider(token, user_reader)

        return id_provider


def setup_providers() -> Iterable[Provider]:
    return [
        gateway_provider(),
        db_provider(),
        interactor_provider(),
        cache_provider(),
        config_provider(),
        infrastructure_provider(),
        service_provider(),
    ]


def setup_http_di() -> AsyncContainer:
    providers = setup_providers()
    providers += [HTTPProvider()]

    container = make_async_container(*providers)

    return container

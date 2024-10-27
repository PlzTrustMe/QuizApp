from abc import abstractmethod
from typing import Any, Protocol, TypeAlias

import jwt
from jwt import PyJWKClient

from app.infrastructure.jwt.config import Auth0Config, JWTConfig
from app.infrastructure.jwt.exception import JWTDecodeError, JWTExpiredError

JWTPayload: TypeAlias = dict[str, Any]
JWTToken: TypeAlias = str


class JWTProcessor(Protocol):
    @abstractmethod
    def encode(self, payload: JWTPayload) -> JWTToken: ...

    @abstractmethod
    def decode(self, token: JWTToken) -> JWTPayload: ...

    @abstractmethod
    def decode_oauth(self, token: JWTToken) -> JWTPayload: ...


class PyJWTProcessor(JWTProcessor):
    def __init__(self, jwt_config: JWTConfig, auth0_config: Auth0Config):
        self.jwt_config = jwt_config
        self.auth0_config = auth0_config

    def encode(self, payload: JWTPayload) -> JWTToken:
        return jwt.encode(
            payload, self.jwt_config.key, self.jwt_config.algorithm
        )

    def decode(self, token: JWTToken) -> JWTPayload:
        try:
            return jwt.decode(
                token,
                self.jwt_config.key,
                algorithms=[self.jwt_config.algorithm],
            )
        except jwt.ExpiredSignatureError as exc:
            raise JWTExpiredError from exc
        except jwt.DecodeError as exc:
            raise JWTDecodeError from exc

    def decode_oauth(self, token: JWTToken) -> JWTPayload:
        jwt_client = PyJWKClient(
            f"https://{self.auth0_config.domain}/.well-known/jwks.json"
        )

        key = jwt_client.get_signing_key_from_jwt(token)

        try:
            return jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=self.auth0_config.audience,
            )
        except jwt.ExpiredSignatureError as exc:
            raise JWTExpiredError from exc
        except jwt.DecodeError as exc:
            raise JWTDecodeError from exc

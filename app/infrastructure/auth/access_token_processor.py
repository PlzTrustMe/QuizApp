from datetime import UTC, datetime

from app.core.commands.errors import (
    AccessTokenIsExpiredError,
    UnauthorizedError,
)
from app.core.commands.sign_in import AccessTokenData
from app.infrastructure.jwt.exception import JWTDecodeError, JWTExpiredError
from app.infrastructure.jwt.jwt_processor import JWTProcessor, JWTToken


class AccessTokenProcessor:
    def __init__(self, jwt_processor: JWTProcessor):
        self.jwt_processor = jwt_processor

    def encode(self, token: AccessTokenData) -> JWTToken:
        token_payload = {
            "sub": {"email": token.email},
            "exp": token.expires_in,
        }

        token = self.jwt_processor.encode(token_payload)

        return token

    def decode(self, token: JWTToken) -> AccessTokenData:
        try:
            payload = self.jwt_processor.decode(token)
            sub = payload["sub"]

            email = str(sub["email"])
            expires_in = datetime.fromtimestamp(float(payload["exp"]), UTC)

            data = AccessTokenData(email=email, expires_in=expires_in)
        except JWTExpiredError as exc:
            raise AccessTokenIsExpiredError from exc
        except (JWTDecodeError, ValueError, TypeError, KeyError) as exc:
            raise UnauthorizedError from exc
        else:
            return data

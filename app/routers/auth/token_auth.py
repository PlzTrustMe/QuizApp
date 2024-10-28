from fastapi import Request, Response

from app.core.commands.user.errors import UnauthorizedError
from app.core.commands.user.sign_in import AccessTokenData
from app.infrastructure.auth.access_token_processor import AccessTokenProcessor
from app.routers.auth.config import TokenAuthConfig


class TokenAuth:
    def __init__(
        self,
        request: Request,
        token_processor: AccessTokenProcessor,
        config: TokenAuthConfig,
    ):
        self.request = request
        self.token_processor = token_processor
        self.config = config

    def set_session(
        self, token: AccessTokenData, response: Response
    ) -> Response:
        jwt_token = self.token_processor.encode(token)

        response.set_cookie(
            self.config.token_cookies_key, jwt_token, httponly=True
        )

        return response

    def get_access_token(self) -> AccessTokenData:
        cookies = self.request.cookies
        token_key = self.config.token_cookies_key
        cookies_token = cookies.get(token_key)

        if not cookies_token:
            raise UnauthorizedError()

        token = self.token_processor.decode(cookies_token)

        return token

    def get_token_data(self, token: str) -> AccessTokenData:
        return self.token_processor.decode_oauth(token)

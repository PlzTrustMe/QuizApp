from fastapi import Request, Response

from app.core.commands.sign_in import SignInOutputData
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
        self, token: SignInOutputData, response: Response
    ) -> Response:
        jwt_token = self.token_processor.encode(token)

        response.set_cookie(
            self.config.token_cookies_key, jwt_token, httponly=True
        )

        return response

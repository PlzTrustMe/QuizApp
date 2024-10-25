from fastapi import Request, Response

from app.core.commands.sign_in import SignInOutputData
from app.infrastructure.auth.access_token_processor import AccessTokenProcessor


class TokenAuth:
    def __init__(
        self, request: Request, token_processor: AccessTokenProcessor
    ):
        self.request = request
        self.token_processor = token_processor

    def set_session(
        self, token: SignInOutputData, response: Response
    ) -> Response:
        jwt_token = self.token_processor.encode(token)

        response.set_cookie("token", jwt_token, httponly=True)

        return response

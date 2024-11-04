from app.core.commands.user.errors import UnauthorizedError, UserNotFoundError
from app.core.commands.user.sign_in import AccessTokenData
from app.core.entities.user import User
from app.core.entities.value_objects import UserEmail
from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.user_gateways import (
    UserGateway,
)


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        token: AccessTokenData,
        user_gateway: UserGateway,
    ):
        self.token = token
        self.user_gateway = user_gateway

    async def get_user(self) -> User:
        user_email = self.token.email

        user = await self.user_gateway.by_email(UserEmail(user_email))
        if not user:
            raise UnauthorizedError from UserNotFoundError

        return user

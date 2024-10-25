from app.core.commands.errors import UnauthorizedError, UserNotFoundError
from app.core.commands.sign_in import AccessTokenData
from app.core.entities.value_objects import UserEmail
from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.user_gateways import (
    UserDetail,
    UserReader,
)


class TokenIdProvider(IdProvider):
    def __init__(
        self,
        token: AccessTokenData,
        user_reader: UserReader,
    ):
        self.token = token
        self.user_reader = user_reader

    async def get_user(self) -> UserDetail:
        user_email = self.token.email

        user = await self.user_reader.by_email(UserEmail(user_email))
        if not user:
            raise UnauthorizedError from UserNotFoundError

        return user

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from app.core.commands.user.errors import (
    UserNotFoundByEmailError,
)
from app.core.entities.value_objects import (
    ExpiresIn,
    UserEmail,
    UserRawPassword,
)
from app.core.interfaces.password_hasher import PasswordHasher
from app.core.interfaces.user_gateways import UserGateway


@dataclass(frozen=True)
class SignInInputData:
    email: str
    password: str


@dataclass(frozen=True)
class AccessTokenData:
    email: str
    expires_in: datetime


@dataclass
class SignIn:
    user_gateway: UserGateway
    password_hasher: PasswordHasher

    async def __call__(self, data: SignInInputData) -> AccessTokenData:
        email = UserEmail(data.email)
        user_pwd = UserRawPassword(data.password)

        user = await self.user_gateway.by_email(email)
        if not user:
            raise UserNotFoundByEmailError(data.email)

        self.password_hasher.verify_password(user_pwd, user.hashed_password)

        now = datetime.now(tz=UTC)
        expires_in = ExpiresIn(now + timedelta(minutes=30))

        return AccessTokenData(
            email=user.email.to_row(), expires_in=expires_in.to_raw()
        )

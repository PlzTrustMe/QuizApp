import logging
from dataclasses import dataclass

from app.core.commands.user.errors import UserEmailAlreadyExistError
from app.core.common.commiter import Commiter
from app.core.entities.user import User
from app.core.entities.value_objects import (
    FullName,
    UserEmail,
    UserRawPassword,
)
from app.core.interfaces.password_hasher import PasswordHasher
from app.core.interfaces.user_gateways import UserGateway


@dataclass(frozen=True)
class SignUpInputData:
    email: str
    password: str
    first_name: str
    last_name: str


@dataclass(frozen=True)
class SignUpOutputData:
    user_id: int


@dataclass
class SignUp:
    user_gateway: UserGateway
    password_hasher: PasswordHasher
    commiter: Commiter

    async def __call__(self, data: SignUpInputData) -> SignUpOutputData:
        email = UserEmail(data.email)
        raw_password = UserRawPassword(data.password)
        full_name = FullName(
            first_name=data.first_name, last_name=data.last_name
        )

        if await self.user_gateway.is_exist(data.email):
            raise UserEmailAlreadyExistError(data.email)

        hashed_password = self.password_hasher.hash_password(raw_password)

        user = User(
            user_id=None,
            full_name=full_name,
            email=email,
            hashed_password=hashed_password,
        )

        await self.user_gateway.add(user)

        await self.commiter.commit()

        logging.info("Create user with email=%s", email)

        return SignUpOutputData(user_id=user.user_id)

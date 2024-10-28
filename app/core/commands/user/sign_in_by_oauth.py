import logging
from dataclasses import dataclass

from app.core.common.commiter import Commiter
from app.core.entities.user import User
from app.core.entities.value_objects import UserEmail
from app.core.interfaces.user_gateways import UserGateway


@dataclass(frozen=True)
class SignInByOauthInputData:
    email: str


@dataclass
class SignInByOauth:
    user_gateway: UserGateway
    commiter: Commiter

    async def __call__(self, data: SignInByOauthInputData):
        email = UserEmail(data.email)

        if await self.user_gateway.by_email(email):
            logging.info("User with email %s successfully sign in", data.email)
            return

        new_user = User(
            user_id=None, full_name=None, email=email, hashed_password=None
        )

        await self.user_gateway.add(new_user)

        await self.commiter.commit()

        logging.info("Create new user with email=%s", data.email)

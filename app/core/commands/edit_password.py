import logging
from dataclasses import dataclass

from app.core.commands.errors import UserNotFoundError
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.user import UserId
from app.core.entities.value_objects import UserRawPassword
from app.core.interfaces.password_hasher import PasswordHasher
from app.core.interfaces.user_gateways import UserGateway


@dataclass(frozen=True)
class EditPasswordInputData:
    user_id: int
    old_password: str
    new_password: str


@dataclass
class EditPassword:
    user_gateway: UserGateway
    password_hasher: PasswordHasher
    access_service: AccessService
    commiter: Commiter

    async def __call__(self, data: EditPasswordInputData) -> None:
        user = await self.user_gateway.by_id(UserId(data.user_id))
        if not user:
            raise UserNotFoundError(data.user_id)

        self.password_hasher.verify_password(
            UserRawPassword(data.old_password), user.hashed_password
        )

        await self.access_service.ensure_can_edit_password(user)

        hashed_password = self.password_hasher.hash_password(
            UserRawPassword(data.new_password)
        )

        user.hashed_password = hashed_password

        await self.commiter.commit()

        logging.info("User with id=%s edit him password", data.user_id)

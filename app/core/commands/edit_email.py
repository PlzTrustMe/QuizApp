import logging
from dataclasses import dataclass

from app.core.commands.errors import (
    UserEmailAlreadyExistError,
    UserNotFoundError,
)
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.user import UserId
from app.core.entities.value_objects import UserEmail
from app.core.interfaces.user_gateways import UserGateway


@dataclass(frozen=True)
class EditEmailInputData:
    user_id: int
    new_email: str


@dataclass
class EditEmail:
    user_gateway: UserGateway
    access_service: AccessService
    commiter: Commiter

    async def __call__(self, data: EditEmailInputData) -> None:
        email = UserEmail(data.new_email)

        user = await self.user_gateway.by_id(UserId(data.user_id))
        if not user:
            raise UserNotFoundError(data.user_id)

        await self.access_service.ensure_can_edit_email(user)

        if await self.user_gateway.is_exist(data.new_email):
            raise UserEmailAlreadyExistError(data.new_email)

        user.email = email

        await self.commiter.commit()

        logging.info(
            "User with id=%s edit email %s", user.user_id, data.new_email
        )

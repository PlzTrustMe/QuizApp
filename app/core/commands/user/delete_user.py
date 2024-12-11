import logging
from dataclasses import dataclass

from app.core.commands.user.errors import UserNotFoundError
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.user import UserId
from app.core.interfaces.user_gateways import UserGateway


@dataclass(frozen=True)
class DeleteUserInputData:
    user_id: int


@dataclass
class DeleteUser:
    user_gateway: UserGateway
    commiter: Commiter
    access_service: AccessService

    async def __call__(self, data: DeleteUserInputData) -> None:
        user_id = UserId(data.user_id)

        user = await self.user_gateway.by_id(user_id)
        if not user:
            raise UserNotFoundError(data.user_id)

        await self.access_service.ensure_can_delete_user(user)

        await self.user_gateway.delete(user_id)

        await self.commiter.commit()

        logging.info("User with id=%s was delete", user_id)

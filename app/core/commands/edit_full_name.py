import logging
from dataclasses import dataclass

from app.core.commands.errors import UserNotFoundError
from app.core.common.commiter import Commiter
from app.core.entities.user import UserId
from app.core.interfaces.user_gateways import UserGateway


@dataclass(frozen=True)
class EditFullNameInputData:
    user_id: int
    first_name: str
    last_name: str


@dataclass(frozen=True)
class EditFullNameOutputData:
    user_id: int


@dataclass
class EditFullName:
    user_gateway: UserGateway
    commiter: Commiter

    async def __call__(
        self, data: EditFullNameInputData
    ) -> EditFullNameOutputData:
        user = await self.user_gateway.by_id(UserId(data.user_id))
        if not user:
            raise UserNotFoundError(data.user_id)

        user.full_name = user.full_name.edit(data.first_name, data.last_name)

        await self.commiter.commit()

        logging.info("User with id=%s update full name", data.user_id)

        return EditFullNameOutputData(user_id=user.user_id)

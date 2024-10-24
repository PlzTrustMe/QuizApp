from dataclasses import dataclass

from app.core.commands.errors import UserNotFoundError
from app.core.entities.user import UserId
from app.core.interfaces.user_gateways import UserDetail, UserReader


@dataclass(frozen=True)
class GetUserByIdInputData:
    user_id: int


@dataclass
class GetUserById:
    user_reader: UserReader

    async def __call__(self, data: GetUserByIdInputData) -> UserDetail:
        user = await self.user_reader.by_id(UserId(data.user_id))
        if not user:
            raise UserNotFoundError(data.user_id)

        return user

from dataclasses import dataclass

from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.user_gateways import UserDetail, UserReader


@dataclass
class GetMe:
    id_provider: IdProvider
    user_reader: UserReader

    async def __call__(self) -> UserDetail:
        actor = await self.id_provider.get_user()

        return await self.user_reader.by_id(actor.user_id)

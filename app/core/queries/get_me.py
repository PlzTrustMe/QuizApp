from dataclasses import dataclass

from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.user_gateways import UserDetail


@dataclass
class GetMe:
    id_provider: IdProvider

    async def __call__(self) -> UserDetail:
        user = await self.id_provider.get_user()

        return user

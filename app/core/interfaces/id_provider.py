from abc import abstractmethod
from asyncio import Protocol

from app.core.interfaces.user_gateways import UserDetail


class IdProvider(Protocol):
    @abstractmethod
    async def get_user(self) -> UserDetail: ...

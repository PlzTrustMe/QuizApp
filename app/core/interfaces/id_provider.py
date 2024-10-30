from abc import abstractmethod
from asyncio import Protocol

from app.core.entities.user import User


class IdProvider(Protocol):
    @abstractmethod
    async def get_user(self) -> User: ...

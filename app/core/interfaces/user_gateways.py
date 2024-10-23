from abc import abstractmethod
from asyncio import Protocol

from app.core.entities.user import User, UserId


class UserGateway(Protocol):
    @abstractmethod
    async def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def is_exist(self, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def by_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError

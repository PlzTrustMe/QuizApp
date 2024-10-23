from abc import abstractmethod
from asyncio import Protocol
from dataclasses import dataclass
from typing import Iterable

from app.core.common.pagination import Pagination
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

    @abstractmethod
    async def delete(self, user_id: UserId) -> None:
        raise NotImplementedError


@dataclass
class UserDetail:
    user_id: int
    email: str
    full_name: str


@dataclass
class UserFilters:
    is_active: bool | None = None


class UserReader(Protocol):
    @abstractmethod
    async def by_id(self, user_id: UserId) -> UserDetail | None:
        raise NotImplementedError

    @abstractmethod
    async def get_users(
        self, filters: UserFilters, pagination: Pagination
    ) -> Iterable[UserDetail]:
        raise NotImplementedError

    @abstractmethod
    async def total(self, filters: UserFilters) -> int:
        raise NotImplementedError

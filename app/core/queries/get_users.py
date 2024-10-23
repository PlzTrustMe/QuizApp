import asyncio
from dataclasses import dataclass

from app.core.common.pagination import Pagination
from app.core.interfaces.user_gateways import (
    UserDetail,
    UserFilters,
    UserReader,
)


@dataclass(frozen=True)
class GetUsersInputData:
    filters: UserFilters
    pagination: Pagination


@dataclass(frozen=True)
class GetUsersOutputData:
    total: int
    users: list[UserDetail]


@dataclass
class GetUsers:
    user_reader: UserReader

    async def __call__(self, data: GetUsersInputData) -> GetUsersOutputData:
        total = await asyncio.create_task(self.user_reader.total(data.filters))
        users = await asyncio.create_task(
            self.user_reader.get_users(data.filters, data.pagination)
        )

        return GetUsersOutputData(total=total, users=users)

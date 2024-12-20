import logging
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
        total = await self.user_reader.total(data.filters)
        users = await self.user_reader.get_users(data.filters, data.pagination)

        logging.info("Get users, total=%s", total)

        return GetUsersOutputData(total=total, users=users)

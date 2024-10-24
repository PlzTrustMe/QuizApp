from typing import Iterable

from sqlalchemy import RowMapping, Select, delete, exists, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.errors import UnexpectedError
from app.core.common.pagination import Pagination, SortOrder
from app.core.entities.user import User, UserId
from app.core.interfaces.user_gateways import (
    UserDetail,
    UserFilters,
    UserGateway,
    UserReader,
)
from app.infrastructure.persistence.models.user import users_table


class UserMapper(UserGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_exist(self, email: str) -> bool:
        query = select(exists().where(users_table.c.user_email == email))

        result = await self.session.execute(query)

        return result.scalar()

    async def add(self, user: User) -> None:
        self.session.add(user)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error

    async def by_id(self, user_id: UserId) -> User | None:
        query = select(User).where(users_table.c.user_id == user_id)

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def delete(self, user_id: UserId) -> None:
        query = delete(User).where(users_table.c.user_id == user_id)

        await self.session.execute(query)


class SQLAlchemyUserReader(UserReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _load_user(self, row: RowMapping) -> UserDetail:
        return UserDetail(
            user_id=row.user_id,
            email=row.user_email,
            full_name=f"{row.first_name} {row.last_name}",
        )

    def _make_filters(self, query: Select, filters: UserFilters) -> Select:
        if filters.is_active is not None:
            query = query.where(users_table.c.is_active == filters.is_active)

        return query

    async def by_id(self, user_id: UserId) -> UserDetail | None:
        query = select(
            users_table.c.user_id,
            users_table.c.user_email,
            users_table.c.first_name,
            users_table.c.last_name,
        ).where(users_table.c.user_id == user_id)

        result = await self.session.execute(query)

        row = result.mappings().one_or_none()

        return None if not row else self._load_user(row)

    async def get_users(
        self, filters: UserFilters, pagination: Pagination
    ) -> Iterable[UserDetail]:
        query = select(
            users_table.c.user_id,
            users_table.c.user_email,
            users_table.c.first_name,
            users_table.c.last_name,
        )

        if filters:
            query = self._make_filters(query, filters)

        if pagination.order is SortOrder.ASC:
            query = query.order_by(users_table.c.created_at.asc())
        else:
            query = query.order_by(users_table.c.created_at.desc())

        if pagination.offset is not None:
            query = query.offset(pagination.offset)
        if pagination.limit is not None:
            query = query.limit(pagination.limit)

        result = await self.session.execute(query)

        return [self._load_user(row) for row in result.mappings()]

    async def total(self, filters: UserFilters) -> int:
        query = select(func.count(users_table.c.user_id))

        if filters:
            query = self._make_filters(query, filters)

        total: int = await self.session.scalar(query)

        return total

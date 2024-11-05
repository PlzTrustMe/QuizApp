from sqlalchemy import RowMapping, Select, and_, delete, exists, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.user.errors import UnexpectedError
from app.core.common.pagination import Pagination, SortOrder
from app.core.entities.company import (
    Company,
    CompanyId,
    CompanyUser,
    CompanyUserId,
)
from app.core.entities.user import UserId
from app.core.entities.value_objects import CompanyName
from app.core.interfaces.company_gateways import (
    CompanyDetail,
    CompanyFilters,
    CompanyGateway,
    CompanyReader,
    CompanyUserDetail,
    CompanyUserFilters,
    CompanyUserGateway,
    CompanyUserReader,
)
from app.infrastructure.persistence.models.company import companies_table
from app.infrastructure.persistence.models.company_user import (
    company_users_table,
)


class CompanyMapper(CompanyGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, company: Company) -> None:
        self.session.add(company)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error

    async def is_exist(self, name: CompanyName) -> bool:
        query = select(
            exists().where(companies_table.c.company_name == name.value)
        )

        result = await self.session.execute(query)

        return result.scalar()

    async def by_id(self, company_id: CompanyId) -> Company | None:
        query = select(Company).where(
            companies_table.c.company_id == company_id
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def delete(self, company_id: CompanyId) -> None:
        query = delete(Company).where(
            companies_table.c.company_id == company_id
        )

        await self.session.execute(query)


class CompanyUserMapper(CompanyUserGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, company_user: CompanyUser) -> None:
        self.session.add(company_user)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error

    async def is_exist(self, company_id: CompanyId, user_id: UserId) -> bool:
        query = select(
            exists().where(
                and_(
                    company_users_table.c.company_id == company_id,
                    company_users_table.c.user_id == user_id,
                )
            )
        )

        result = await self.session.execute(query)

        return result.scalar()

    async def by_company(
        self, company_id: CompanyId, user_id: UserId
    ) -> CompanyUser | None:
        query = select(CompanyUser).where(
            and_(
                company_users_table.c.user_id == user_id,
                company_users_table.c.company_id == company_id,
            )
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def by_id(
        self, company_user_id: CompanyUserId
    ) -> CompanyUser | None:
        query = select(CompanyUser).where(
            company_users_table.c.company_user_id == company_user_id
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def delete(self, company_user_id: CompanyUserId) -> None:
        query = delete(CompanyUser).where(
            company_users_table.c.company_user_id == company_user_id
        )

        await self.session.execute(query)


class SQLAlchemyCompanyReader(CompanyReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _load_company(self, row: RowMapping) -> CompanyDetail:
        return CompanyDetail(
            company_id=row.company_id,
            name=row.company_name,
            description=row.company_description,
            visibility=row.visibility,
        )

    def _make_filters(self, query: Select, filters: CompanyFilters) -> Select:
        if filters.visibility is not None:
            query = query.where(
                companies_table.c.visibility == filters.visibility
            )

        return query

    async def by_id(self, company_id: CompanyId) -> CompanyDetail:
        query = select(
            companies_table.c.company_id,
            companies_table.c.company_name,
            companies_table.c.company_description,
            companies_table.c.visibility,
        ).where(companies_table.c.company_id == company_id)

        result = await self.session.execute(query)

        row = result.mappings().one_or_none()

        return self._load_company(row) if row else None

    async def many(
        self, filters: CompanyFilters, pagination: Pagination
    ) -> list[CompanyDetail]:
        query = select(
            companies_table.c.company_id,
            companies_table.c.company_name,
            companies_table.c.company_description,
            companies_table.c.visibility,
        )

        if filters:
            query = self._make_filters(query, filters)

        if pagination.order is SortOrder.ASC:
            query = query.order_by(companies_table.c.created_at.asc())
        else:
            query = query.order_by(companies_table.c.created_at.desc())

        if pagination.offset is not None:
            query = query.offset(pagination.offset)
        if pagination.limit is not None:
            query = query.limit(pagination.limit)

        result = await self.session.execute(query)

        return [self._load_company(row) for row in result.mappings()]

    async def total(self, filters: CompanyFilters) -> int:
        query = select(func.count(companies_table.c.company_id))

        if filters:
            query = self._make_filters(query, filters)

        total: int = await self.session.scalar(query)

        return total


class SQLAlchemyCompanyUserReader(CompanyUserReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _load_model(self, row: RowMapping) -> CompanyUserDetail:
        return CompanyUserDetail(
            company_user_id=row.company_user_id,
            company_id=row.company_id,
            user_id=row.user_id,
            role=row.role,
        )

    def _make_filters(
        self, query: Select, filters: CompanyUserFilters
    ) -> Select:
        if filters.company_role:
            query = query.where(
                company_users_table.c.role == filters.company_role
            )

        return query

    async def by_id(self, company_user_id: CompanyUserId) -> CompanyUserDetail:
        query = select(
            company_users_table.c.company_user_id,
            company_users_table.c.company_id,
            company_users_table.c.user_id,
            company_users_table.c.role,
        ).where(company_users_table.c.company_user_id == company_user_id)

        result = await self.session.execute(query)
        row = result.mappings().one_or_none()

        return None if not row else self._load_model(row)

    async def many(
        self, filters: CompanyUserFilters, pagination: Pagination
    ) -> list[CompanyUserDetail]:
        query = select(
            company_users_table.c.company_user_id,
            company_users_table.c.company_id,
            company_users_table.c.user_id,
            company_users_table.c.role,
        ).where(company_users_table.c.company_id == filters.company_id)

        query = self._make_filters(query, filters)

        if pagination.order is SortOrder.ASC:
            query = query.order_by(company_users_table.c.created_at.asc())
        else:
            query = query.order_by(company_users_table.c.created_at.desc())

        if pagination.offset is not None:
            query = query.offset(pagination.offset)
        if pagination.limit is not None:
            query = query.limit(pagination.limit)

        result = await self.session.execute(query)

        return [self._load_model(row) for row in result.mappings()]

    async def total(self, filters: CompanyUserFilters) -> int:
        query = select(func.count(company_users_table.c.company_user_id))
        query = query.where(
            company_users_table.c.company_id == filters.company_id
        )

        query = self._make_filters(query, filters)

        total: int = await self.session.scalar(query)

        return total

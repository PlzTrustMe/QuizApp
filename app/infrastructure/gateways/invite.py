from sqlalchemy import RowMapping, Select, and_, exists, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.user.errors import UnexpectedError
from app.core.common.pagination import Pagination, SortOrder
from app.core.entities.company import CompanyId
from app.core.entities.invitation import (
    Invitation,
    InvitationId,
    UserRequest,
    UserRequestId,
)
from app.core.entities.user import UserId
from app.core.interfaces.invitation_gateways import (
    InvitationDetail,
    InvitationFilters,
    InvitationGateway,
    InvitationReader,
    UserRequestDetail,
    UserRequestFilters,
    UserRequestGateway,
    UserRequestReader,
)
from app.infrastructure.persistence.models.invite import (
    invitations_table,
    user_requests_table,
)


class InvitationMapper(InvitationGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_exist(self, company_id: CompanyId, user_id: UserId) -> bool:
        query = select(
            exists().where(
                and_(
                    invitations_table.c.company_id == company_id,
                    invitations_table.c.user_id == user_id,
                )
            )
        )

        result = await self.session.execute(query)

        return result.scalar()

    async def add(self, invitation: Invitation) -> None:
        self.session.add(invitation)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error

    async def by_id(self, invitation_id: InvitationId) -> Invitation | None:
        query = select(Invitation).where(
            invitations_table.c.invitation_id == invitation_id
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()


class UserRequestMapper(UserRequestGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_exist(self, company_id: CompanyId, user_id: UserId) -> bool:
        query = select(
            exists().where(
                and_(
                    user_requests_table.c.company_id == company_id,
                    user_requests_table.c.user_id == user_id,
                )
            )
        )

        result = await self.session.execute(query)

        return result.scalar()

    async def add(self, user_request: UserRequest) -> None:
        self.session.add(user_request)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error

    async def by_id(
        self, user_request_id: UserRequestId
    ) -> UserRequest | None:
        query = select(UserRequest).where(
            user_requests_table.c.user_request_id == user_request_id
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()


class SQLAlchemyInvitationReader(InvitationReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _load_model(self, row: RowMapping) -> InvitationDetail:
        return InvitationDetail(
            company_id=row.company_id,
            invitation_id=row.invitation_id,
            status=row.status,
        )

    def _make_filters(
        self, query: Select, filters: InvitationFilters
    ) -> Select:
        if filters.user_id:
            query = query.where(invitations_table.c.user_id == filters.user_id)

        if filters.company_id:
            query = query.where(
                invitations_table.c.company_id == filters.company_id
            )

        return query

    async def many(
        self, filters: InvitationFilters, pagination: Pagination
    ) -> list[InvitationDetail]:
        query = select(
            invitations_table.c.company_id,
            invitations_table.c.invitation_id,
            invitations_table.c.status,
        )

        query = self._make_filters(query, filters)

        if pagination.order is SortOrder.ASC:
            query = query.order_by(invitations_table.c.created_at.asc())
        else:
            query = query.order_by(invitations_table.c.created_at.desc())

        if pagination.offset is not None:
            query = query.offset(pagination.offset)
        if pagination.limit is not None:
            query = query.limit(pagination.limit)

        result = await self.session.execute(query)

        return [self._load_model(row) for row in result.mappings()]

    async def total(self, filters: InvitationFilters) -> int:
        query = select(func.count(invitations_table.c.invitation_id))

        query = self._make_filters(query, filters)

        total: int = await self.session.scalar(query)

        return total


class SQLAlchemyUserRequestReader(UserRequestReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _load_model(self, row: RowMapping) -> UserRequestDetail:
        return UserRequestDetail(
            company_id=row.company_id,
            user_request_id=row.user_request_id,
            status=row.status,
        )

    def _make_filters(
        self, query: Select, filters: UserRequestFilters
    ) -> Select:
        if filters.user_id:
            query = query.where(
                user_requests_table.c.user_id == filters.user_id
            )

        if filters.company_id:
            query = query.where(
                user_requests_table.c.company_id == filters.company_id
            )

        return query

    async def many(
        self, filters: UserRequestFilters, pagination: Pagination
    ) -> list[UserRequestDetail]:
        query = select(
            user_requests_table.c.company_id,
            user_requests_table.c.user_request_id,
            user_requests_table.c.status,
        )

        query = self._make_filters(query, filters)

        if pagination.order is SortOrder.ASC:
            query = query.order_by(user_requests_table.c.created_at.asc())
        else:
            query = query.order_by(user_requests_table.c.created_at.desc())

        if pagination.offset is not None:
            query = query.offset(pagination.offset)
        if pagination.limit is not None:
            query = query.limit(pagination.limit)

        result = await self.session.execute(query)

        return [self._load_model(row) for row in result.mappings()]

    async def total(self, filters: UserRequestFilters) -> int:
        query = select(func.count(user_requests_table.c.user_request_id))

        query = self._make_filters(query, filters)

        total: int = await self.session.scalar(query)

        return total

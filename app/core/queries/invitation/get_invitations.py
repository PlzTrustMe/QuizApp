from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.commands.user.errors import AccessDeniedError
from app.core.common.pagination import Pagination
from app.core.entities.company import CompanyId
from app.core.interfaces.company_gateways import CompanyGateway
from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.invitation_gateways import (
    InvitationDetail,
    InvitationFilters,
    InvitationReader,
)


@dataclass(frozen=True)
class InputData:
    pagination: Pagination


@dataclass(frozen=True)
class GetInvitationByOwner(InputData):
    company_id: int


@dataclass(frozen=True)
class GetInvitationByUser(InputData):
    pass


@dataclass(frozen=True)
class GetInvitationOutputData:
    total: int
    invitations: list[InvitationDetail]


@dataclass
class GetInvitations:
    id_provider: IdProvider
    invitation_reader: InvitationReader
    company_gateway: CompanyGateway

    async def by_user(
        self, data: GetInvitationByUser
    ) -> GetInvitationOutputData:
        user = await self.id_provider.get_user()

        filters = InvitationFilters(user_id=user.user_id)

        return await self._data_processing(filters, data.pagination)

    async def by_owner(
        self, data: GetInvitationByOwner
    ) -> GetInvitationOutputData:
        user = await self.id_provider.get_user()

        company = await self.company_gateway.by_id(CompanyId(data.company_id))
        if not company:
            raise CompanyNotFoundError(user.user_id)
        if company.owner_id != user.user_id:
            raise AccessDeniedError()

        filters = InvitationFilters(company_id=company.company_id)

        return await self._data_processing(filters, data.pagination)

    async def _data_processing(
        self, filters: InvitationFilters, pagination: Pagination
    ) -> GetInvitationOutputData:
        invitations = await self.invitation_reader.many(filters, pagination)
        total = await self.invitation_reader.total(filters)

        return GetInvitationOutputData(total, invitations)

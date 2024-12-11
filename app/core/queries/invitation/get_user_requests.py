from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.commands.user.errors import AccessDeniedError
from app.core.common.pagination import Pagination
from app.core.entities.company import CompanyId
from app.core.interfaces.company_gateways import CompanyGateway
from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.invitation_gateways import (
    UserRequestDetail,
    UserRequestFilters,
    UserRequestReader,
)


@dataclass(frozen=True)
class InputData:
    pagination: Pagination


@dataclass(frozen=True)
class GetUserRequestsByOwner(InputData):
    company_id: int


@dataclass(frozen=True)
class GetUserRequestsByUser(InputData):
    pass


@dataclass(frozen=True)
class GetUserRequestsOutputData:
    total: int
    requests: list[UserRequestDetail]


@dataclass
class GetUserRequests:
    user_request_reader: UserRequestReader
    id_provider: IdProvider
    company_gateway: CompanyGateway

    async def by_user(
        self, data: GetUserRequestsByUser
    ) -> GetUserRequestsOutputData:
        user = await self.id_provider.get_user()

        filters = UserRequestFilters(user_id=user.user_id)

        return await self._data_processing(filters, data.pagination)

    async def by_owner(
        self, data: GetUserRequestsByOwner
    ) -> GetUserRequestsOutputData:
        user = await self.id_provider.get_user()

        company = await self.company_gateway.by_id(CompanyId(data.company_id))
        if not company:
            raise CompanyNotFoundError(data.company_id)
        if company.owner_id != user.user_id:
            raise AccessDeniedError()

        filters = UserRequestFilters(company_id=company.company_id)

        return await self._data_processing(filters, data.pagination)

    async def _data_processing(
        self, filters: UserRequestFilters, pagination: Pagination
    ) -> GetUserRequestsOutputData:
        requests = await self.user_request_reader.many(filters, pagination)
        total = await self.user_request_reader.total(filters)

        return GetUserRequestsOutputData(total, requests)

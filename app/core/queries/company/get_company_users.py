from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.common.pagination import Pagination
from app.core.entities.company import CompanyId
from app.core.interfaces.company_gateways import (
    CompanyGateway,
    CompanyUserDetail,
    CompanyUserFilters,
    CompanyUserReader,
)


@dataclass(frozen=True)
class GetCompanyUsersInputData:
    filters: CompanyUserFilters
    pagination: Pagination


@dataclass(frozen=True)
class GetCompanyUsersOutputData:
    total: int
    users: list[CompanyUserDetail]


@dataclass
class GetCompanyUsers:
    company_gateway: CompanyGateway
    company_user_reader: CompanyUserReader

    async def __call__(
        self, data: GetCompanyUsersInputData
    ) -> GetCompanyUsersOutputData:
        company = await self.company_gateway.by_id(
            CompanyId(data.filters.company_id)
        )
        if not company:
            raise CompanyNotFoundError(data.filters.company_id)

        users = await self.company_user_reader.many(
            data.filters, data.pagination
        )
        total = await self.company_user_reader.total(data.filters)

        return GetCompanyUsersOutputData(total, users)

from dataclasses import dataclass

from app.core.common.pagination import Pagination
from app.core.interfaces.company_gateways import (
    CompanyDetail,
    CompanyFilters,
    CompanyReader,
)


@dataclass(frozen=True)
class GetManyCompaniesInputData:
    filters: CompanyFilters
    pagination: Pagination


@dataclass(frozen=True)
class GetManyCompaniesOutputData:
    total: int
    companies: list[CompanyDetail]


@dataclass
class GetManyCompanies:
    company_reader: CompanyReader

    async def __call__(
        self, data: GetManyCompaniesInputData
    ) -> GetManyCompaniesOutputData:
        total = await self.company_reader.total(data.filters)
        companies = await self.company_reader.many(
            data.filters, data.pagination
        )

        return GetManyCompaniesOutputData(total, companies)

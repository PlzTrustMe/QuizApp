from dataclasses import dataclass

from app.core.entities.company import CompanyId
from app.core.interfaces.company_gateways import CompanyDetail, CompanyReader


@dataclass
class GetCompanyByIdInputData:
    company_id: int


@dataclass
class GetCompanyById:
    company_reader: CompanyReader

    async def __call__(
        self, data: GetCompanyByIdInputData
    ) -> CompanyDetail | None:
        return await self.company_reader.by_id(CompanyId(data.company_id))

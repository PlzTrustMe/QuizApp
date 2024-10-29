from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.entities.company import CompanyId
from app.core.interfaces.company_gateways import CompanyDetail, CompanyReader


@dataclass
class GetCompanyByIdInputData:
    company_id: int


@dataclass
class GetCompanyById:
    company_reader: CompanyReader

    async def __call__(self, data: GetCompanyByIdInputData) -> CompanyDetail:
        company = await self.company_reader.by_id(CompanyId(data.company_id))

        if not company:
            raise CompanyNotFoundError(data.company_id)

        return company

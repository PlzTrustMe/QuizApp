import logging
from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.company import CompanyId
from app.core.interfaces.company_gateways import CompanyGateway


@dataclass(frozen=True)
class DeleteCompanyInputData:
    company_id: int


@dataclass
class DeleteCompany:
    company_gateway: CompanyGateway
    access_service: AccessService
    commiter: Commiter

    async def __call__(self, data: DeleteCompanyInputData) -> None:
        company = await self.company_gateway.by_id(CompanyId(data.company_id))
        if not company:
            raise CompanyNotFoundError(data.company_id)

        await self.access_service.ensure_can_edit_company(company)

        await self.company_gateway.delete(CompanyId(data.company_id))

        await self.commiter.commit()

        logging.info("Company with id=%s successfully delete", data.company_id)

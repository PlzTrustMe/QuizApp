import logging
from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.company import CompanyId
from app.core.entities.value_objects import CompanyName
from app.core.interfaces.company_gateways import CompanyGateway


@dataclass(frozen=True)
class EditCompanyNameInputData:
    company_id: int
    name: str


@dataclass
class EditCompanyName:
    company_gateway: CompanyGateway
    access_service: AccessService
    commiter: Commiter

    async def __call__(self, data: EditCompanyNameInputData) -> None:
        new_name = CompanyName(data.name)

        company = await self.company_gateway.by_id(CompanyId(data.company_id))
        if not company:
            raise CompanyNotFoundError(data.company_id)

        await self.access_service.ensure_can_edit_company(company)

        company.name = new_name

        await self.commiter.commit()

        logging.info(
            "Company with id %s edit name on - %s", data.company_id, data.name
        )

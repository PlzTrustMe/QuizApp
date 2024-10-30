import logging
from dataclasses import dataclass

from app.core.commands.company.errors import (
    CompanyNotFoundError,
    CompanyUserNotFoundError,
)
from app.core.common.commiter import Commiter
from app.core.entities.company import CompanyId
from app.core.entities.user import UserId
from app.core.interfaces.company_gateways import (
    CompanyGateway,
    CompanyUserGateway,
)


@dataclass(frozen=True)
class LeaveFromCompanyInputData:
    company_id: int
    user_id: int


@dataclass
class LeaveFromCompany:
    company_gateway: CompanyGateway
    company_user_gateway: CompanyUserGateway
    commiter: Commiter

    async def __call__(self, data: LeaveFromCompanyInputData) -> None:
        company_id = CompanyId(data.company_id)
        user_id = UserId(data.user_id)

        company = await self.company_gateway.by_id(company_id)
        if not company:
            raise CompanyNotFoundError(company_id)
        company_user = await self.company_user_gateway.by_identity(user_id)
        if not company_user:
            raise CompanyUserNotFoundError()

        await self.company_user_gateway.delete(company_user.company_user_id)

        await self.commiter.commit()

        logging.info(
            "User with id %s leave from company %s", user_id, company_id
        )

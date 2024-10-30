import logging
from dataclasses import dataclass

from app.core.commands.company.errors import (
    CompanyWithNameAlreadyExistError,
)
from app.core.common.commiter import Commiter
from app.core.entities.company import (
    Company,
    CompanyId,
    CompanyRole,
    CompanyUser,
    Visibility,
)
from app.core.entities.user import UserId
from app.core.entities.value_objects import CompanyDescription, CompanyName
from app.core.interfaces.company_gateways import (
    CompanyGateway,
    CompanyUserGateway,
)
from app.core.interfaces.id_provider import IdProvider


@dataclass(frozen=True)
class CreateCompanyInputData:
    name: str
    description: str


@dataclass
class CreateCompany:
    id_provider: IdProvider
    company_gateway: CompanyGateway
    company_user_gateway: CompanyUserGateway
    commiter: Commiter

    async def __call__(self, data: CreateCompanyInputData) -> CompanyId:
        company_name = CompanyName(data.name)
        company_description = CompanyDescription(data.description)

        user = await self.id_provider.get_user()

        if await self.company_gateway.is_exist(company_name):
            raise CompanyWithNameAlreadyExistError(company_name.value)

        new_company = Company(
            company_id=None,
            owner_id=UserId(user.user_id),
            name=company_name,
            description=company_description,
            visibility=Visibility.VISIBLE,
        )

        await self.company_gateway.add(new_company)

        new_company_user = CompanyUser(
            company_user_id=None,
            company_id=new_company.company_id,
            user_id=UserId(user.user_id),
            role=CompanyRole.OWNER,
        )

        await self.company_user_gateway.add(new_company_user)

        await self.commiter.commit()

        logging.info("New company - %s was created", data.name)

        return new_company.company_id

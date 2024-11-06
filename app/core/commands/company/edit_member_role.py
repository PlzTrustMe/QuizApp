import logging
from dataclasses import dataclass

from app.core.commands.company.errors import (
    CompanyNotFoundError,
    CompanyUserNotFoundError,
)
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.company import CompanyId, CompanyRole
from app.core.entities.user import UserId
from app.core.interfaces.company_gateways import (
    CompanyGateway,
    CompanyUserGateway,
)


@dataclass
class EditMemberRoleInputData:
    user_id: int
    company_id: int
    new_role: CompanyRole


@dataclass
class EditMemberRole:
    access_service: AccessService
    company_user_gateway: CompanyUserGateway
    company_gateway: CompanyGateway
    commiter: Commiter

    async def __call__(self, data: EditMemberRoleInputData):
        user_id = UserId(data.user_id)
        company_id = CompanyId(data.company_id)

        company = await self.company_gateway.by_id(company_id)
        if not company:
            raise CompanyNotFoundError(company_id)

        member = await self.company_user_gateway.by_company(
            company_id, user_id
        )
        if not member:
            raise CompanyUserNotFoundError()

        await self.access_service.ensure_can_edit_member_role(company)

        member.role = data.new_role

        await self.commiter.commit()

        logging.info(
            "Edit role to member %s, new role - %s",
            member.company_user_id,
            data.new_role,
        )

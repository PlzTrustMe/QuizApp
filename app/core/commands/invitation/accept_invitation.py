import logging
from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.commands.invitation.errors import InvitationNotFoundError
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.company import CompanyRole, CompanyUser
from app.core.entities.invitation import InvitationId, RequestStatus
from app.core.interfaces.company_gateways import (
    CompanyGateway,
    CompanyUserGateway,
)
from app.core.interfaces.invitation_gateways import InvitationGateway


@dataclass(frozen=True)
class AcceptInvitationInputData:
    invitation_id: int


@dataclass
class AcceptInvitation:
    access_service: AccessService
    invitation_gateway: InvitationGateway
    company_gateway: CompanyGateway
    company_user_gateway: CompanyUserGateway
    commiter: Commiter

    async def __call__(self, data: AcceptInvitationInputData) -> None:
        invitation_id = InvitationId(data.invitation_id)

        invitation = await self.invitation_gateway.by_id(invitation_id)
        if not invitation:
            raise InvitationNotFoundError(invitation_id)
        company = await self.company_gateway.by_id(invitation.company_id)
        if not company:
            raise CompanyNotFoundError(invitation.company_id)

        await self.access_service.ensure_can_accept_invitation(invitation)

        invitation.status = RequestStatus.ACCEPTED

        company_user = CompanyUser(
            company_user_id=None,
            company_id=company.company_id,
            user_id=invitation.user_id,
            role=CompanyRole.MEMBER,
        )

        await self.company_user_gateway.add(company_user)

        await self.commiter.commit()

        logging.info("Invitation with id %s was accepted", invitation_id)

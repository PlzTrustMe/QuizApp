import logging
from dataclasses import dataclass

from app.core.commands.invitation.errors import InvitationNotFoundError
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.invitation import InvitationId, RequestStatus
from app.core.interfaces.company_gateways import CompanyGateway
from app.core.interfaces.invitation_gateways import InvitationGateway


@dataclass(frozen=True)
class RejectInvitationInputData:
    invitation_id: int


@dataclass
class RejectInvitation:
    access_service: AccessService
    invitation_gateway: InvitationGateway
    company_gateway: CompanyGateway
    commiter: Commiter

    async def __call__(self, data: RejectInvitationInputData) -> None:
        invitation_id = InvitationId(data.invitation_id)

        invitation = await self.invitation_gateway.by_id(invitation_id)
        if not invitation:
            raise InvitationNotFoundError(invitation_id)
        company = await self.company_gateway.by_id(invitation.company_id)

        await self.access_service.ensure_can_reject_invitation(
            company, invitation
        )

        invitation.status = RequestStatus.REJECTED

        await self.commiter.commit()

        logging.info("Invitation with id %s was rejected", invitation_id)

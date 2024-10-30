import logging
from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.commands.invitation.errors import InvitationAlreadyExistError
from app.core.commands.user.errors import UserNotFoundError
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.company import CompanyId
from app.core.entities.invitation import Invitation, InvitationId
from app.core.entities.user import UserId
from app.core.interfaces.company_gateways import (
    CompanyGateway,
)
from app.core.interfaces.invitation_gateways import InvitationGateway
from app.core.interfaces.user_gateways import UserGateway


@dataclass(frozen=True)
class SendInvitationToUserInputData:
    company_id: int
    user_id: int


@dataclass
class SendInvitationToUser:
    access_service: AccessService
    invitation_gateway: InvitationGateway
    company_gateway: CompanyGateway
    user_gateway: UserGateway
    commiter: Commiter

    async def __call__(
        self, data: SendInvitationToUserInputData
    ) -> InvitationId:
        company = await self.company_gateway.by_id(CompanyId(data.company_id))
        if not company:
            raise CompanyNotFoundError(data.company_id)

        user = await self.user_gateway.by_id(UserId(data.user_id))
        if not user:
            raise UserNotFoundError(data.user_id)

        if await self.invitation_gateway.is_exist(
            company.company_id, user.user_id
        ):
            raise InvitationAlreadyExistError(company.company_id, user.user_id)

        await self.access_service.ensure_can_send_invitation(company, user)

        new_invitation = Invitation(
            invitation_id=None,
            company_id=CompanyId(data.company_id),
            user_id=UserId(data.user_id),
        )
        await self.invitation_gateway.add(new_invitation)

        await self.commiter.commit()

        logging.info(
            "Successfully send invitation from company %s to user %s",
            data.company_id,
            data.user_id,
        )

        return new_invitation.invitation_id

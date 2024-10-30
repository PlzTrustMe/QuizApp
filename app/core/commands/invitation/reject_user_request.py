import logging
from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.commands.invitation.errors import UserRequestNotFoundError
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.invitation import RequestStatus, UserRequestId
from app.core.interfaces.company_gateways import CompanyGateway
from app.core.interfaces.invitation_gateways import UserRequestGateway


@dataclass(frozen=True)
class RejectUserRequestInputData:
    request_id: int


@dataclass
class RejectUserRequest:
    access_service: AccessService
    user_request_gateway: UserRequestGateway
    company_gateway: CompanyGateway
    commiter: Commiter

    async def __call__(self, data: RejectUserRequestInputData) -> None:
        user_request_id = UserRequestId(data.request_id)

        user_request = await self.user_request_gateway.by_id(user_request_id)
        if not user_request:
            raise UserRequestNotFoundError(user_request_id)
        company = await self.company_gateway.by_id(user_request.company_id)
        if not company:
            raise CompanyNotFoundError(user_request.company_id)

        await self.access_service.ensure_can_reject_user_request(
            company, user_request.user_id
        )

        user_request.status = RequestStatus.REJECTED

        await self.commiter.commit()

        logging.info("User request with id %s was rejected", user_request_id)

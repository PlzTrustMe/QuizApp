import logging
from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.commands.invitation.errors import UserRequestNotFoundError
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.company import CompanyRole, CompanyUser
from app.core.entities.invitation import RequestStatus, UserRequestId
from app.core.interfaces.company_gateways import (
    CompanyGateway,
    CompanyUserGateway,
)
from app.core.interfaces.invitation_gateways import UserRequestGateway


@dataclass(frozen=True)
class AcceptUserRequestInputData:
    user_request_id: int


@dataclass
class AcceptUserRequest:
    user_request_gateway: UserRequestGateway
    company_gateway: CompanyGateway
    access_service: AccessService
    company_user: CompanyUserGateway
    commiter: Commiter

    async def __call__(self, data: AcceptUserRequestInputData) -> None:
        user_request_id = UserRequestId(data.user_request_id)

        user_request = await self.user_request_gateway.by_id(user_request_id)
        if not user_request:
            raise UserRequestNotFoundError(user_request_id)
        company = await self.company_gateway.by_id(user_request.company_id)
        if not company:
            raise CompanyNotFoundError(user_request.company_id)

        await self.access_service.ensure_can_accept_user_request(
            user_request, company
        )

        user_request.status = RequestStatus.ACCEPTED

        company_user = CompanyUser(
            company_user_id=None,
            company_id=company.company_id,
            user_id=user_request.user_id,
            role=CompanyRole.MEMBER,
        )
        await self.company_user.add(company_user)

        await self.commiter.commit()

        logging.info("User request with id %s was accepted", user_request_id)

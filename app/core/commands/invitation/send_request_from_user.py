import logging
from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.commands.invitation.errors import UserRequestAlreadyExistError
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.company import CompanyId
from app.core.entities.invitation import UserRequest, UserRequestId
from app.core.interfaces.company_gateways import CompanyGateway
from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.invitation_gateways import UserRequestGateway


@dataclass(frozen=True)
class SendRequestFromUserInputData:
    company_id: int


@dataclass
class SendRequestFromUser:
    id_provider: IdProvider
    access_service: AccessService
    company_gateway: CompanyGateway
    user_request_gateway: UserRequestGateway
    commiter: Commiter

    async def __call__(
        self, data: SendRequestFromUserInputData
    ) -> UserRequestId:
        user = await self.id_provider.get_user()

        company = await self.company_gateway.by_id(CompanyId(data.company_id))
        if not company:
            raise CompanyNotFoundError(data.company_id)

        await self.access_service.ensure_can_send_request(company, user)
        if await self.user_request_gateway.is_exist(
            company.company_id, user.user_id
        ):
            raise UserRequestAlreadyExistError(
                company.company_id, user.user_id
            )

        user_request = UserRequest(
            user_request_id=None,
            company_id=company.company_id,
            user_id=user.user_id,
        )

        await self.user_request_gateway.add(user_request)
        await self.commiter.commit()

        logging.info(
            "Successfully send request from user %s to company %s",
            user.user_id,
            company.company_id,
        )

        return user_request.user_request_id

from app.core.commands.invitation.errors import CompanyUserAlreadyExistError
from app.core.commands.user.errors import AccessDeniedError
from app.core.entities.company import Company, CompanyId
from app.core.entities.invitation import Invitation, UserRequest
from app.core.entities.user import User, UserId
from app.core.interfaces.company_gateways import CompanyUserGateway
from app.core.interfaces.id_provider import IdProvider


class AccessService:
    def __init__(
        self, id_provider: IdProvider, company_user_gateway: CompanyUserGateway
    ):
        self.id_provider = id_provider
        self.company_user_gateway = company_user_gateway

    async def _is_identity(self, user_id: UserId):
        actor = await self.id_provider.get_user()

        if user_id != actor.user_id:
            raise AccessDeniedError()

    async def _is_owner(self, company: Company):
        actor = await self.id_provider.get_user()

        if company.owner_id != actor.user_id:
            raise AccessDeniedError()

    async def _is_not_company_member(
        self, company_id: CompanyId, user_id: UserId
    ):
        if await self.company_user_gateway.is_exist(company_id, user_id):
            raise CompanyUserAlreadyExistError(company_id, user_id)

    async def ensure_can_edit_full_name(self, record_to_edit: User):
        await self._is_identity(record_to_edit.user_id)

    async def ensure_can_edit_password(self, record_to_edit: User):
        await self._is_identity(record_to_edit.user_id)

    async def ensure_can_delete_user(self, record_to_edit: User):
        await self._is_identity(record_to_edit.user_id)

    async def ensure_can_edit_company(self, company: Company):
        await self._is_owner(company)

    async def ensure_can_send_invitation(self, company: Company, user: User):
        await self._is_owner(company)
        await self._is_not_company_member(company.company_id, user.user_id)

    async def ensure_can_reject_invitation(
        self, company: Company, invitation: Invitation
    ):
        try:
            await self._is_owner(company)
        except AccessDeniedError:
            await self._is_identity(invitation.user_id)

    async def ensure_can_accept_invitation(self, invitation: Invitation):
        await self._is_identity(invitation.user_id)
        await self._is_not_company_member(
            invitation.company_id, invitation.user_id
        )

    async def ensure_can_send_request(self, company: Company, user: User):
        await self._is_not_company_member(company.company_id, user.user_id)

    async def ensure_can_reject_user_request(
        self, company: Company, user_id: UserId
    ):
        try:
            await self._is_owner(company)
        except AccessDeniedError:
            await self._is_identity(user_id)

    async def ensure_can_accept_user_request(
        self, user_request: UserRequest, company: Company
    ):
        await self._is_owner(company)
        await self._is_not_company_member(
            user_request.company_id, user_request.user_id
        )

    async def ensure_can_delete_from_company(self, company: Company):
        await self._is_owner(company)

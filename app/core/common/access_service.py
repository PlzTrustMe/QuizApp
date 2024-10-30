from app.core.commands.invitation.errors import CompanyUserAlreadyExistError
from app.core.commands.user.errors import AccessDeniedError
from app.core.entities.company import Company
from app.core.entities.user import User
from app.core.interfaces.company_gateways import CompanyUserGateway
from app.core.interfaces.id_provider import IdProvider


class AccessService:
    def __init__(
        self, id_provider: IdProvider, company_user_gateway: CompanyUserGateway
    ):
        self.id_provider = id_provider
        self.company_user_gateway = company_user_gateway

    async def _is_identity(self, record_to_edit: User):
        actor = await self.id_provider.get_user()

        if record_to_edit.user_id != actor.user_id:
            raise AccessDeniedError()

    async def _is_owner(self, company: Company):
        actor = await self.id_provider.get_user()

        if company.owner_id != actor.user_id:
            raise AccessDeniedError()

    async def _is_not_company_member(self, company: Company, user: User):
        if await self.company_user_gateway.is_exist(
            company.company_id, user.user_id
        ):
            raise CompanyUserAlreadyExistError(
                company.company_id, user.user_id
            )

    async def ensure_can_edit_full_name(self, record_to_edit: User):
        await self._is_identity(record_to_edit)

    async def ensure_can_edit_password(self, record_to_edit: User):
        await self._is_identity(record_to_edit)

    async def ensure_can_delete_user(self, record_to_edit: User):
        await self._is_identity(record_to_edit)

    async def ensure_can_edit_company(self, company: Company):
        await self._is_owner(company)

    async def ensure_can_send_invitation(self, company: Company, user: User):
        await self._is_owner(company)
        await self._is_not_company_member(company, user)

    async def ensure_can_send_request(self, company: Company, user: User):
        await self._is_not_company_member(company, user)

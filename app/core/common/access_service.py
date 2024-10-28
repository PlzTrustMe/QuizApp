from app.core.commands.user.errors import AccessDeniedError
from app.core.entities.company import Company
from app.core.entities.user import User
from app.core.interfaces.id_provider import IdProvider


class AccessService:
    def __init__(self, id_provider: IdProvider):
        self.id_provider = id_provider

    async def _is_identity(self, record_to_edit: User):
        actor = await self.id_provider.get_user()

        if record_to_edit.user_id != actor.user_id:
            raise AccessDeniedError()

    async def _is_owner(self, company: Company):
        actor = await self.id_provider.get_user()

        if company.owner_id != actor.user_id:
            raise AccessDeniedError()

    async def ensure_can_edit_full_name(self, record_to_edit: User):
        await self._is_identity(record_to_edit)

    async def ensure_can_edit_password(self, record_to_edit: User):
        await self._is_identity(record_to_edit)

    async def ensure_can_delete_user(self, record_to_edit: User):
        await self._is_identity(record_to_edit)

    async def ensure_can_edit_company(self, company: Company):
        await self._is_owner(company)

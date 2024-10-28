from app.core.commands.errors import AccessDeniedError
from app.core.entities.user import User
from app.core.interfaces.id_provider import IdProvider


class AccessService:
    def __init__(self, id_provider: IdProvider):
        self.id_provider = id_provider

    async def ensure_can_edit_full_name(self, record_to_edit: User):
        actor = await self.id_provider.get_user()

        if record_to_edit.user_id != actor.user_id:
            raise AccessDeniedError()

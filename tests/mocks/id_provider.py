from app.core.entities.user import User
from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.user_gateways import UserDetail


class FakeIdProvider(IdProvider):
    def __init__(self, user: User):
        self.requested = False
        self.user = user

    async def get_user(self) -> UserDetail:
        self.requested = True
        return UserDetail(
            user_id=self.user.user_id,
            email=self.user.email.to_row(),
            full_name=self.user.full_name.full_name,
        )

from app.core.common.pagination import Pagination
from app.core.entities.user import User, UserId
from app.core.interfaces.user_gateways import (
    UserDetail,
    UserFilters,
    UserGateway,
    UserReader,
)


class FakeUserMapper(UserGateway):
    def __init__(self, user: User):
        self.user = user
        self.saved = False
        self.deleted = False

    async def add(self, user: User) -> None:
        self.user.email = user.email
        self.user.full_name = user.full_name
        self.user.hashed_password = user.hashed_password

        self.saved = True

    async def is_exist(self, email: str) -> bool:
        return self.user.email.to_row() == email

    async def by_id(self, user_id: UserId) -> User | None:
        if self.user.user_id != user_id:
            return None
        return self.user

    async def delete(self, user_id: UserId) -> None:
        if self.user.user_id == user_id:
            self.deleted = True


class FakeUserReader(UserReader):
    def __init__(self, user: User):
        self.users = [user]

    def _map_to_dto(self, user: User) -> UserDetail:
        return UserDetail(
            user_id=user.user_id,
            email=str(user.email),
            full_name=str(user.full_name),
        )

    def _filter_user(self, user: User, filters: UserFilters) -> bool:
        if filters.is_active is None:
            return True
        return user.is_active == filters.is_active

    async def by_id(self, user_id: UserId) -> UserDetail | None:
        for user in self.users:
            if user.user_id == user_id:
                return self._map_to_dto(user)
        return None

    async def total(self, filters: UserFilters) -> int:
        return len(
            [user for user in self.users if self._filter_user(user, filters)]
        )

    async def get_users(
        self, filters: UserFilters, pagination: Pagination
    ) -> list[UserDetail]:
        filtered_users = [
            user for user in self.users if self._filter_user(user, filters)
        ]

        offset = pagination.offset if pagination.offset else 0
        limit = pagination.limit if pagination.limit else 1000

        end = offset + limit

        return [self._map_to_dto(user) for user in filtered_users[offset:end]]

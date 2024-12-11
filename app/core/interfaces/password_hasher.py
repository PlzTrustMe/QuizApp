from abc import abstractmethod
from asyncio import Protocol

from app.core.entities.value_objects import UserRawPassword


class PasswordHasher(Protocol):
    @abstractmethod
    def hash_password(self, raw_password: UserRawPassword) -> str: ...

    @abstractmethod
    def verify_password(
        self, raw_password: UserRawPassword, hashed_password: str
    ) -> None: ...

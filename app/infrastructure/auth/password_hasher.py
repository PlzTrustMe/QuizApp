import argon2

from app.core.commands.errors import PasswordMismatchError
from app.core.entities.value_objects import UserRawPassword
from app.core.interfaces.password_hasher import PasswordHasher


class ArgonPasswordHasher(PasswordHasher):
    def __init__(self, password_hasher: argon2.PasswordHasher):
        self.ph = password_hasher

    def hash_password(self, raw_password: UserRawPassword) -> str:
        return self.ph.hash(raw_password.password)

    def verify_password(
        self, raw_password: UserRawPassword, hashed_password: str
    ) -> None:
        try:
            self.ph.verify(hashed_password, raw_password.password)
        except argon2.exceptions.VerifyMismatchError as error:
            raise PasswordMismatchError(raw_password.password) from error

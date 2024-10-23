import argon2

from app.core.entities.value_objects import UserRawPassword
from app.core.interfaces.password_hasher import PasswordHasher


class ArgonPasswordHasher(PasswordHasher):
    def __init__(self, password_hasher: argon2.PasswordHasher):
        self.ph = password_hasher

    def hash_password(self, raw_password: UserRawPassword) -> str:
        return self.ph.hash(raw_password.password)

from dataclasses import dataclass

from app.core.common.base_error import BaseError


@dataclass(eq=False)
class UnexpectedError(BaseError):
    pass


@dataclass(eq=False)
class UserEmailAlreadyExistError(BaseError):
    email: str

    @property
    def message(self) -> str:
        return f"User with email {self.email} already exist"

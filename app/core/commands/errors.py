from dataclasses import dataclass

from app.core.common.base_error import ApplicationError


@dataclass(eq=False)
class UnexpectedError(ApplicationError):
    pass


@dataclass(eq=False)
class UserEmailAlreadyExistError(ApplicationError):
    email: str

    @property
    def message(self) -> str:
        return f"User with email {self.email} already exist"


@dataclass
class UserNotFoundError(ApplicationError):
    user_id: int

    @property
    def message(self) -> str:
        return f"User with id={self.user_id} not found"

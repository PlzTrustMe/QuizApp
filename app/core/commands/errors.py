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


@dataclass(eq=False)
class UserNotFoundError(ApplicationError):
    user_id: int

    @property
    def message(self) -> str:
        return f"User with id={self.user_id} not found"


@dataclass(eq=False)
class UserNotFoundByEmailError(ApplicationError):
    email: str

    @property
    def message(self) -> str:
        return f"User with email={self.email} not found"


@dataclass(eq=False)
class PasswordMismatchError(ApplicationError):
    password: str

    @property
    def message(self) -> str:
        return f"Password - {self.password} mismatch"


@dataclass(eq=False)
class AccessTokenIsExpiredError(ApplicationError):
    @property
    def message(self) -> str:
        return "Token is expired"


@dataclass(eq=False)
class UnauthorizedError(ApplicationError):
    @property
    def message(self) -> str:
        return "Unauthorized"

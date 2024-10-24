from dataclasses import dataclass

from app.core.common.base_error import ApplicationError


@dataclass(eq=False)
class FirstNameTooLongError(ApplicationError):
    first_name: str

    @property
    def message(self):
        return f"The name is too long - {self.first_name[:15]}"


@dataclass(eq=False)
class LastNameTooLongError(ApplicationError):
    last_name: str

    @property
    def message(self):
        return f"The lastname is too long - {self.last_name[:15]}"


@dataclass(eq=False)
class EmptyError(ApplicationError):
    @property
    def message(self):
        return "Can't be empty"


@dataclass(eq=False)
class InvalidUserEmailError(ApplicationError):
    email: str

    @property
    def message(self):
        return f"Invalid user email {self.email}"


@dataclass(eq=False)
class WeakPasswordError(ApplicationError):
    error: str

    @property
    def message(self):
        return f"Invalid user password, error - {self.error}"

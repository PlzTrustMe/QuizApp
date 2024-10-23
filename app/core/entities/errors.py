from dataclasses import dataclass

from app.core.common.base_error import BaseError


@dataclass(eq=False)
class FirstNameTooLongError(BaseError):
    first_name: str

    @property
    def message(self):
        return f"The name is too long - {self.first_name[:15]}"


@dataclass(eq=False)
class LastNameTooLongError(BaseError):
    last_name: str

    @property
    def message(self):
        return f"The lastname is too long - {self.last_name[:15]}"


@dataclass(eq=False)
class EmptyError(BaseError):
    @property
    def message(self):
        return "Can't be empty"


@dataclass(eq=False)
class InvalidUserEmailError(BaseError):
    @property
    def message(self):
        return "Invalid user email"

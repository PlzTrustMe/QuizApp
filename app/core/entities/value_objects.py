from dataclasses import dataclass

from pydantic import validate_email
from pydantic_core import PydanticCustomError

from app.core.entities.errors import (
    EmptyError,
    FirstNameTooLongError,
    InvalidUserEmailError,
    LastNameTooLongError,
)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class FullName:
    first_name: str
    last_name: str

    def __post_init__(self) -> None:
        max_length = 15

        if not self.first_name or not self.last_name:
            raise EmptyError()
        if len(self.first_name) > max_length:
            raise FirstNameTooLongError(self.first_name)
        if len(self.last_name) > max_length:
            raise LastNameTooLongError(self.last_name)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class UserEmail:
    email: str

    MAX_LENGTH = 100
    MIN_LENGTH = 6

    def __post_init__(self) -> None:
        try:
            validate_email(self.email)
        except PydanticCustomError as error:
            raise InvalidUserEmailError() from error

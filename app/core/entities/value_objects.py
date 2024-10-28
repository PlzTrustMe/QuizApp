import re
from dataclasses import dataclass
from datetime import UTC, datetime

from email_validator import EmailNotValidError, validate_email

from app.core.entities.errors import (
    EmptyError,
    FirstNameTooLongError,
    InvalidUserEmailError,
    LastNameTooLongError,
    WeakPasswordError,
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

    @classmethod
    def edit(cls, first_name: str, last_name: str) -> "FullName":
        return cls(first_name, last_name)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class UserEmail:
    email: str

    MAX_LENGTH = 100
    MIN_LENGTH = 6

    def __post_init__(self) -> None:
        try:
            validate_email(self.email, check_deliverability=False)
        except EmailNotValidError as error:
            raise InvalidUserEmailError(self.email) from error

    def __str__(self) -> str:
        return self.email

    def to_row(self) -> str:
        return self.email


def has_special_symbols(string: str) -> bool:
    regex = re.compile("[@_!#$%^&*()<>?/}{~:]")

    return re.search(regex, string) is not None


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class UserRawPassword:
    password: str

    def __post_init__(self) -> None:
        error_messages = {
            "The password must contain a capital letter.": lambda s: any(
                x.isupper() for x in s
            ),
            "The password must contain a number.": lambda s: any(
                x.isdigit() for x in s
            ),
            "The password must not contain spaces.": lambda s: not any(
                x.isspace() for x in s
            ),
            "The password must contain a "
            "special character (@, #, $, %)": has_special_symbols,
            "The password should "
            "not consist only of capital letters.": lambda s: any(
                x.islower() for x in s
            ),
        }

        for message, password_validator in error_messages.items():
            if not password_validator(self.password):
                raise WeakPasswordError(message)

    def to_raw(self):
        return self.password


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class ExpiresIn:
    value: datetime

    @property
    def is_expired(self) -> bool:
        now = datetime.now(tz=UTC)

        return now > self.value

    def to_raw(self):
        return self.value

import pytest

from app.core.entities.errors import (
    EmptyError,
    FirstNameTooLongError,
    InvalidUserEmailError,
    LastNameTooLongError,
    WeakPasswordError,
)
from app.core.entities.value_objects import (
    FullName,
    UserEmail,
    UserRawPassword,
)


@pytest.mark.parametrize(
    ["first_name", "last_name", "exc_class"],
    [
        ("Test", "Testovich", None),
        ("", "Testovich", EmptyError),
        ("A" * 16, "Testovich", FirstNameTooLongError),
        ("Test", "B" * 16, LastNameTooLongError),
    ],
)
def test_full_name(first_name: str, last_name: str, exc_class) -> None:
    if exc_class:
        with pytest.raises(exc_class):
            FullName(first_name, last_name)
    else:
        full_name = FullName(first_name, last_name)

        assert isinstance(full_name, FullName)
        assert full_name.first_name == first_name
        assert full_name.last_name == last_name


@pytest.mark.parametrize(
    "email",
    [
        "abc",
        "a" * 120,
        "myawesomeemail@gmail",
        "............@gmail.com",
        "myemailgmail.com",
        "my email@gmail.com",
        "              ",
        12345,
    ],
)
def test_create_user_bad_email(email):
    with pytest.raises(InvalidUserEmailError):
        UserEmail(str(email))


@pytest.mark.parametrize(
    "pwd",
    [
        "qwerty",
        "qwertyA",
        "qwertyA1",
    ],
)
def test_create_user_bad_password(pwd):
    with pytest.raises(WeakPasswordError):
        UserRawPassword(pwd)

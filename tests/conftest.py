import argon2
import pytest

from app.core.entities.user import User, UserId
from app.core.entities.value_objects import (
    FullName,
    UserEmail,
    UserRawPassword,
)
from app.core.interfaces.password_hasher import PasswordHasher
from app.infrastructure.auth.password_hasher import ArgonPasswordHasher


@pytest.fixture
def user_email() -> UserEmail:
    return UserEmail("test@gmail.com")


@pytest.fixture
def user_full_name() -> FullName:
    return FullName("Test", "Testovich")


@pytest.fixture
def user_pwd() -> UserRawPassword:
    return UserRawPassword("someSuper123#Password")


@pytest.fixture
def user_fake_id() -> UserId:
    return UserId(1)


@pytest.fixture
def password_hasher() -> PasswordHasher:
    return ArgonPasswordHasher(argon2.PasswordHasher())


@pytest.fixture
def user(
    password_hasher: PasswordHasher,
    user_email: UserEmail,
    user_pwd: UserRawPassword,
    user_fake_id: UserId,
    user_full_name: FullName,
) -> User:
    hashed_password = password_hasher.hash_password(user_pwd)

    return User(user_fake_id, user_full_name, user_email, hashed_password)

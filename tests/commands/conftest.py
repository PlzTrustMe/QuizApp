import pytest

from app.core.entities.user import User
from tests.mocks.commiter import FakeCommiter
from tests.mocks.user_gateways import FakeUserMapper


@pytest.fixture
def user_gateway(user: User) -> FakeUserMapper:
    return FakeUserMapper(user=user)


@pytest.fixture
def commiter() -> FakeCommiter:
    return FakeCommiter()

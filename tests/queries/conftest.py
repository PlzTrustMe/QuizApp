import pytest

from app.core.entities.user import User
from tests.mocks.user_gateways import FakeUserReader


@pytest.fixture
def user_reader(user: User) -> FakeUserReader:
    return FakeUserReader(user=user)

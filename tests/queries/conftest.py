import pytest

from app.core.entities.user import User
from tests.mocks.id_provider import FakeIdProvider
from tests.mocks.user_gateways import FakeUserReader


@pytest.fixture
def user_reader(user: User) -> FakeUserReader:
    return FakeUserReader(user=user)


@pytest.fixture
def id_provider(user: User) -> FakeIdProvider:
    return FakeIdProvider(user)

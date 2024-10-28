import pytest

from app.core.common.access_service import AccessService
from app.core.entities.user import User
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import (
    FakeCompanyMapper,
    FakeCompanyUserMapper,
)
from tests.mocks.id_provider import FakeIdProvider
from tests.mocks.user_gateways import FakeUserMapper


@pytest.fixture
def user_gateway(user: User) -> FakeUserMapper:
    return FakeUserMapper(user=user)


@pytest.fixture
def commiter() -> FakeCommiter:
    return FakeCommiter()


@pytest.fixture
def access_service(id_provider: FakeIdProvider) -> AccessService:
    return AccessService(id_provider)


@pytest.fixture
def company_gateway() -> FakeCompanyMapper:
    return FakeCompanyMapper()


@pytest.fixture
def company_user_gateway() -> FakeCompanyUserMapper:
    return FakeCompanyUserMapper()

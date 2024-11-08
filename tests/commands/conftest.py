import pytest

from app.core.commands.notification.service import NotificationService
from app.core.common.access_service import AccessService
from app.core.entities.user import User
from tests.mocks.cache import FakeCache
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import (
    FakeCompanyMapper,
    FakeCompanyUserMapper,
)
from tests.mocks.id_provider import FakeIdProvider
from tests.mocks.invitation_gateways import (
    FakeInvitationMapper,
    FakeUserRequestMapper,
)
from tests.mocks.notification_gateway import FakeNotificationMapper
from tests.mocks.quiz_gateways import (
    FakeAnswerMapper,
    FakeQuestionMapper,
    FakeQuizMapper,
    FakeQuizParticipationMapper,
    FakeQuizResultMapper,
)
from tests.mocks.user_gateways import FakeUserMapper


@pytest.fixture
def user_gateway(user: User) -> FakeUserMapper:
    return FakeUserMapper(user=user)


@pytest.fixture
def commiter() -> FakeCommiter:
    return FakeCommiter()


@pytest.fixture
def access_service(
    id_provider: FakeIdProvider, company_user_gateway: FakeCompanyUserMapper
) -> AccessService:
    return AccessService(id_provider, company_user_gateway)


@pytest.fixture
def company_gateway() -> FakeCompanyMapper:
    return FakeCompanyMapper()


@pytest.fixture
def company_user_gateway() -> FakeCompanyUserMapper:
    return FakeCompanyUserMapper()


@pytest.fixture
def invitation_gateway() -> FakeInvitationMapper:
    return FakeInvitationMapper()


@pytest.fixture
def user_request_gateway() -> FakeUserRequestMapper:
    return FakeUserRequestMapper()


@pytest.fixture
def quiz_gateway() -> FakeQuizMapper:
    return FakeQuizMapper()


@pytest.fixture
def question_gateway() -> FakeQuestionMapper:
    return FakeQuestionMapper()


@pytest.fixture
def answer_gateway() -> FakeAnswerMapper:
    return FakeAnswerMapper()


@pytest.fixture
def participation_gateway() -> FakeQuizParticipationMapper:
    return FakeQuizParticipationMapper()


@pytest.fixture
def quiz_result_gateway() -> FakeQuizResultMapper:
    return FakeQuizResultMapper()


@pytest.fixture
def cache() -> FakeCache:
    return FakeCache()


@pytest.fixture
def notification_gateway() -> FakeNotificationMapper:
    return FakeNotificationMapper()


@pytest.fixture
def notification_service(
    notification_gateway: FakeNotificationMapper,
    company_user_gateway: FakeCompanyUserMapper,
) -> NotificationService:
    return NotificationService(notification_gateway, company_user_gateway)

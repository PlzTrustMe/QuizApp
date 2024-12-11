import pytest

from app.core.commands.quiz.errors import QuizParticipationNotFoundError
from app.core.commands.quiz.save_quiz_result import (
    SaveQuizResult,
    SaveQuizResultInputData,
)
from tests.mocks.cache import FakeCache
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import FakeCompanyUserMapper
from tests.mocks.id_provider import FakeIdProvider
from tests.mocks.quiz_gateways import (
    FakeQuizMapper,
    FakeQuizParticipationMapper,
    FakeQuizResultMapper,
)


@pytest.mark.parametrize(
    ["participation_id", "exc_class"],
    [(1, None), (2, QuizParticipationNotFoundError)],
)
async def test_save_quiz_result(
    id_provider: FakeIdProvider,
    participation_gateway: FakeQuizParticipationMapper,
    quiz_gateway: FakeQuizMapper,
    company_user_gateway: FakeCompanyUserMapper,
    quiz_result_gateway: FakeQuizResultMapper,
    commiter: FakeCommiter,
    cache: FakeCache,
    participation_id: int,
    exc_class,
) -> None:
    command = SaveQuizResult(
        id_provider,
        participation_gateway,
        quiz_gateway,
        company_user_gateway,
        quiz_result_gateway,
        cache,
        commiter,
    )
    id_provider.user.user_id = 2

    input_data = SaveQuizResultInputData(participation_id, 2)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not quiz_result_gateway.saved
        assert not commiter.commited
        assert not cache.cached
    else:
        await coro

        assert quiz_result_gateway.saved
        assert commiter.commited
        assert cache.cached

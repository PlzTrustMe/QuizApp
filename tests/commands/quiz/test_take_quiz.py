import pytest

from app.core.commands.quiz.errors import QuizNotFoundError
from app.core.commands.quiz.take_quiz import TakeQuiz, TakeQuizInputData
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import FakeCompanyUserMapper
from tests.mocks.id_provider import FakeIdProvider
from tests.mocks.quiz_gateways import (
    FakeQuizMapper,
    FakeQuizParticipationMapper,
)


@pytest.mark.parametrize(
    ["quiz_id", "exc_class"], [(1, None), (2, QuizNotFoundError)]
)
async def test_take_quiz(
    id_provider: FakeIdProvider,
    company_user_gateway: FakeCompanyUserMapper,
    quiz_gateway: FakeQuizMapper,
    participation_gateway: FakeQuizParticipationMapper,
    commiter: FakeCommiter,
    quiz_id: int,
    exc_class,
) -> None:
    command = TakeQuiz(
        id_provider,
        company_user_gateway,
        quiz_gateway,
        participation_gateway,
        commiter,
    )
    id_provider.user.user_id = 2

    input_data = TakeQuizInputData(quiz_id)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not participation_gateway.saved
        assert not commiter.commited
    else:
        await coro

        assert participation_gateway.saved
        assert commiter.commited

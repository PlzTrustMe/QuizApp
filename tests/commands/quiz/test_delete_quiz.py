import pytest

from app.core.commands.quiz.delete_quiz import DeleteQuiz, DeleteQuizInputData
from app.core.commands.quiz.errors import QuizNotFoundError
from app.core.common.access_service import AccessService
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import FakeCompanyMapper
from tests.mocks.quiz_gateways import FakeQuizMapper


@pytest.mark.parametrize(
    ["quiz_id", "exc_class"], [(1, None), (2, QuizNotFoundError)]
)
async def test_delete_quiz(
    quiz_gateway: FakeQuizMapper,
    company_gateway: FakeCompanyMapper,
    access_service: AccessService,
    commiter: FakeCommiter,
    quiz_id: int,
    exc_class,
):
    command = DeleteQuiz(
        quiz_gateway, company_gateway, access_service, commiter
    )
    input_data = DeleteQuizInputData(quiz_id=quiz_id)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not commiter.commited
        assert not quiz_gateway.deleted
    else:
        await coro

        assert commiter.commited
        assert quiz_gateway.deleted

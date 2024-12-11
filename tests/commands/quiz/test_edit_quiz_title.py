from app.core.commands.quiz.edit_quiz_title import (
    EditQuizTitle,
    EditQuizTitleInputData,
)
from app.core.common.access_service import AccessService
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import FakeCompanyMapper
from tests.mocks.quiz_gateways import FakeQuizMapper


async def test_edit_quiz_title(
    quiz_gateway: FakeQuizMapper,
    company_gateway: FakeCompanyMapper,
    access_service: AccessService,
    commiter: FakeCommiter,
) -> None:
    command = EditQuizTitle(
        quiz_gateway, company_gateway, access_service, commiter
    )
    input_data = EditQuizTitleInputData(quiz_id=1, new_title="New Title")

    await command(input_data)

    assert commiter.commited
    assert quiz_gateway.quiz.title == "New Title"

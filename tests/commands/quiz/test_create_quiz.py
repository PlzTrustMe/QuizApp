from app.core.commands.notification.service import NotificationService
from app.core.commands.quiz.create_quiz import (
    AnswerData,
    CreateQuiz,
    CreateQuizInputData,
    QuestionData,
)
from app.core.common.access_service import AccessService
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import FakeCompanyMapper
from tests.mocks.quiz_gateways import (
    FakeAnswerMapper,
    FakeQuestionMapper,
    FakeQuizMapper,
)


async def test_create_quiz(
    access_service: AccessService,
    company_gateway: FakeCompanyMapper,
    quiz_gateway: FakeQuizMapper,
    question_gateway: FakeQuestionMapper,
    answer_gateway: FakeAnswerMapper,
    notification_service: NotificationService,
    commiter: FakeCommiter,
) -> None:
    command = CreateQuiz(
        access_service,
        company_gateway,
        quiz_gateway,
        question_gateway,
        answer_gateway,
        notification_service,
        commiter,
    )

    questions = [
        QuestionData(
            title="Who",
            answers=[
                AnswerData(text="+"),
                AnswerData(text="-", is_correct=True),
            ],
        ),
        QuestionData(
            title="Where",
            answers=[
                AnswerData(text="+", is_correct=True),
                AnswerData(text="-"),
            ],
        ),
    ]

    input_data = CreateQuizInputData(
        company_id=1,
        title="Test Quiz",
        description="Test desc",
        questions=questions,
    )

    await command(input_data)

    assert quiz_gateway.saved
    assert question_gateway.saved
    assert answer_gateway.saved
    assert commiter.commited

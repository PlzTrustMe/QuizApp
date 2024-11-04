from app.core.entities.company import CompanyId
from app.core.entities.quiz import (
    Answer,
    AnswerId,
    Question,
    QuestionId,
    Quiz,
    QuizId,
)
from app.core.interfaces.quiz_gateways import (
    AnswerGateway,
    QuestionGateway,
    QuizGateway,
)


class FakeQuizMapper(QuizGateway):
    def __init__(self):
        self.quiz = Quiz(
            quiz_id=QuizId(1),
            company_id=CompanyId(1),
            title="New quiz",
            description="Quiz description",
        )

        self.saved = False

    async def add(self, quiz: Quiz) -> None:
        self.quiz.title = quiz.title
        self.quiz.description = quiz.description

        self.saved = True

    async def by_id(self, quiz_id: QuizId) -> Quiz | None:
        return self.quiz if self.quiz.quiz_id == quiz_id else None


class FakeQuestionMapper(QuestionGateway):
    def __init__(self):
        self.questions = [
            Question(
                question_id=QuestionId(1),
                quiz_id=QuizId(1),
                title="How are you?",
            ),
            Question(
                question_id=QuestionId(2),
                quiz_id=QuizId(1),
                title="Vilkoy v glaz?",
            ),
        ]

        self.saved = False

    async def add(self, question: Question) -> None:
        self.questions.append(question)

        self.saved = True


class FakeAnswerMapper(AnswerGateway):
    def __init__(self):
        self.answers = [
            Answer(
                answer_id=AnswerId(1),
                question_id=QuestionId(1),
                text="Yes",
            ),
            Answer(
                answer_id=AnswerId(2),
                question_id=QuestionId(1),
                text="No",
                is_correct=True,
            ),
            Answer(
                answer_id=AnswerId(3), question_id=QuestionId(2), text="Yes"
            ),
            Answer(
                answer_id=AnswerId(4),
                question_id=QuestionId(2),
                text="No",
                is_correct=True,
            ),
        ]

        self.saved = False

    async def add_many(self, answers: list[Answer]) -> None:
        self.answers.extend(answers)

        self.saved = True

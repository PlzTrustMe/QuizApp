import logging
from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.commands.quiz.errors import (
    InvalidAnswerQuantityError,
    InvalidAnswersValidateError,
    InvalidQuestionQuantityError,
)
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.company import CompanyId
from app.core.entities.quiz import Answer, Question, Quiz, QuizId
from app.core.interfaces.company_gateways import CompanyGateway
from app.core.interfaces.quiz_gateways import (
    AnswerGateway,
    QuestionGateway,
    QuizGateway,
)


@dataclass(frozen=True)
class AnswerData:
    text: str
    is_correct: bool = False


@dataclass(frozen=True)
class QuestionData:
    title: str
    answers: list[AnswerData]


@dataclass(frozen=True)
class CreateQuizInputData:
    company_id: int
    title: str
    description: str
    questions: list[QuestionData]


@dataclass
class CreateQuiz:
    access_service: AccessService
    company_gateway: CompanyGateway
    quiz_gateway: QuizGateway
    question_gateway: QuestionGateway
    answer_gateway: AnswerGateway
    commiter: Commiter

    async def __call__(self, data: CreateQuizInputData) -> QuizId:
        self._quiz_data_validate(data.questions)

        company_id = CompanyId(data.company_id)

        company = await self.company_gateway.by_id(company_id)
        if not company:
            raise CompanyNotFoundError(company_id)

        await self.access_service.ensure_can_create_quiz(company)

        new_quiz = Quiz(
            quiz_id=None,
            company_id=company_id,
            title=data.title,
            description=data.description,
        )

        await self.quiz_gateway.add(new_quiz)

        await self._add_questions_to_quiz(new_quiz.quiz_id, data.questions)

        await self.commiter.commit()

        logging.info(
            "Create new quiz with id %s for company %s",
            new_quiz.quiz_id,
            company_id,
        )

        return new_quiz.quiz_id

    def _quiz_data_validate(self, questions: list[QuestionData]):
        min_questions = 2
        min_answers = 2
        max_answers = 4

        if len(questions) < min_questions:
            raise InvalidQuestionQuantityError()

        for question in questions:
            if not (min_answers <= len(question.answers) <= max_answers):
                raise InvalidAnswerQuantityError()
            if not any(answer.is_correct for answer in question.answers):
                raise InvalidAnswersValidateError()

    async def _add_questions_to_quiz(
        self, quiz_id: QuizId, questions: list[QuestionData]
    ) -> None:
        for question in questions:
            new_question = Question(
                question_id=None,
                quiz_id=quiz_id,
                title=question.title,
            )

            await self.question_gateway.add(new_question)

            answers = [
                Answer(
                    answer_id=None,
                    question_id=new_question.question_id,
                    text=answer.text,
                    is_correct=answer.is_correct,
                )
                for answer in question.answers
            ]
            await self.answer_gateway.add_many(answers)

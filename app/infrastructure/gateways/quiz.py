from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.user.errors import UnexpectedError
from app.core.entities.quiz import Answer, Question, Quiz, QuizId
from app.core.interfaces.quiz_gateways import (
    AnswerGateway,
    QuestionGateway,
    QuizGateway,
)
from app.infrastructure.persistence.models.quiz import quizzes_table


class QuizMapper(QuizGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, quiz: Quiz) -> None:
        self.session.add(quiz)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error

    async def by_id(self, quiz_id: QuizId) -> Quiz | None:
        query = select(Quiz).where(quizzes_table.c.quiz_id == quiz_id)

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def delete(self, quiz_id: QuizId) -> None:
        query = delete(Quiz).where(quizzes_table.c.quiz_id == quiz_id)

        await self.session.execute(query)


class QuestionMapper(QuestionGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, question: Question) -> None:
        self.session.add(question)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error


class AnswerMapper(AnswerGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_many(self, answers: list[Answer]) -> None:
        self.session.add_all(answers)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error

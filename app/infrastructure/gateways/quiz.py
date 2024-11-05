from sqlalchemy import RowMapping, and_, delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.user.errors import UnexpectedError
from app.core.common.pagination import Pagination, SortOrder
from app.core.entities.quiz import Answer, Question, Quiz, QuizId
from app.core.interfaces.quiz_gateways import (
    AnswerDetail,
    AnswerGateway,
    QuestionDetail,
    QuestionGateway,
    QuizDetail,
    QuizFilters,
    QuizGateway,
    QuizReader,
)
from app.infrastructure.persistence.models.quiz import (
    answers_table,
    questions_table,
    quizzes_table,
)


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


class SQLAlchemyQuizReader(QuizReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _load_model(self, rows: list[RowMapping]) -> list[QuizDetail]:
        quizzes = {}
        for row in rows:
            quiz_id = row["quiz_id"]

            if quiz_id not in quizzes:
                quizzes[quiz_id] = QuizDetail(
                    quiz_id=quiz_id,
                    title=row["title"],
                    description=row["description"],
                    participation_count=row["participation_count"],
                    questions=[],
                )

            question_id = row["question_id"]
            quiz = quizzes[quiz_id]
            question = next(
                (q for q in quiz.questions if q.question_id == question_id),
                None,
            )

            if not question:
                question = QuestionDetail(
                    question_id=question_id,
                    title=row["question_title"],
                    answers=[],
                )
                quiz.questions.append(question)

            answer = AnswerDetail(
                answer_id=row["answer_id"],
                text=row["answer_text"],
                is_correct=row["is_correct"],
            )
            question.answers.append(answer)

        return list(quizzes.values())

    async def get_many(
        self, filters: QuizFilters, pagination: Pagination
    ) -> list[QuizDetail]:
        query = (
            select(
                quizzes_table.c.quiz_id,
                quizzes_table.c.title,
                quizzes_table.c.description,
                quizzes_table.c.participation_count,
                questions_table.c.question_id,
                questions_table.c.title.label("question_title"),
                answers_table.c.answer_id,
                answers_table.c.text.label("answer_text"),
                answers_table.c.is_correct,
            )
            .join(
                questions_table,
                and_(quizzes_table.c.quiz_id == questions_table.c.quiz_id),
            )
            .join(
                answers_table,
                and_(
                    questions_table.c.question_id
                    == answers_table.c.question_id
                ),
            )
        )

        if filters and filters.company_id:
            query = query.where(
                quizzes_table.c.company_id == filters.company_id
            )

        if pagination.order is SortOrder.ASC:
            query = query.order_by(quizzes_table.c.created_at.asc())
        else:
            query = query.order_by(quizzes_table.c.created_at.desc())

        if pagination.offset is not None:
            query = query.offset(pagination.offset)
        if pagination.limit is not None:
            query = query.limit(pagination.limit)

        result = await self.session.execute(query)
        rows = result.mappings().all()

        return self._load_models(list(rows))

    async def total(self, filters: QuizFilters) -> int:
        query = select(func.count(quizzes_table.c.quiz_id))

        if filters and filters.company_id:
            query = query.where(
                quizzes_table.c.company_id == filters.company_id
            )

        total: int = await self.session.scalar(query)

        return total

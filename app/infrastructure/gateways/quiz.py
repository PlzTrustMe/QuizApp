from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Float,
    RowMapping,
    and_,
    between,
    cast,
    delete,
    func,
    select,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.user.errors import UnexpectedError
from app.core.common.pagination import Pagination, SortOrder
from app.core.entities.company import CompanyId, CompanyUserId
from app.core.entities.quiz import (
    Answer,
    Question,
    Quiz,
    QuizId,
    QuizParticipation,
    QuizParticipationId,
    QuizResult,
)
from app.core.entities.user import UserId
from app.core.interfaces.quiz_gateways import (
    AnswerDetail,
    AnswerGateway,
    LastQuizCompletionTimes,
    QuestionDetail,
    QuestionGateway,
    QuizAverage,
    QuizDetail,
    QuizFilters,
    QuizGateway,
    QuizParticipationGateway,
    QuizReader,
    QuizResultGateway,
)
from app.infrastructure.persistence.models.company_user import (
    company_users_table,
)
from app.infrastructure.persistence.models.quiz import (
    answers_table,
    questions_table,
    quiz_participations_table,
    quiz_results_table,
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


class QuizParticipationMapper(QuizParticipationGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, participation: QuizParticipation) -> None:
        self.session.add(participation)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error

    async def by_id(
        self, quiz_participation_id: QuizParticipationId
    ) -> QuizParticipation | None:
        query = select(QuizParticipation).where(
            quiz_participations_table.c.quiz_participation_id
            == quiz_participation_id
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()


class QuizResultMapper(QuizResultGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, quiz_result: QuizResult) -> None:
        self.session.add(quiz_result)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error


class SQLAlchemyQuizReader(QuizReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _load_models(self, rows: list[RowMapping]) -> list[QuizDetail]:
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

    async def total_average_user_score(
        self, company_user_id: CompanyUserId, company_id: CompanyId
    ) -> float:
        total_possible_correct_answers_query = (
            select(func.count(answers_table.c.answer_id))
            .join(
                questions_table,
                and_(
                    questions_table.c.question_id
                    == answers_table.c.question_id
                ),
            )
            .join(
                quizzes_table,
                and_(quizzes_table.c.quiz_id == questions_table.c.quiz_id),
            )
            .where(
                quizzes_table.c.company_id == company_id,
                answers_table.c.is_correct.is_(True),
            )
            .label("total_possible_correct_answers")
        )

        user_correct_answers_query = (
            select(func.count(quiz_results_table.c.correct_answers))
            .join(
                quiz_participations_table,
                and_(
                    quiz_participations_table.c.quiz_participation_id
                    == quiz_results_table.c.quiz_participation_id
                ),
            )
            .where(
                and_(
                    quiz_participations_table.c.company_user_id
                    == company_user_id,
                    quiz_participations_table.c.quiz_id
                    == quizzes_table.c.quiz_id,
                    quizzes_table.c.company_id == company_id,
                )
            )
            .label("user_correct_answers")
        )

        query = select(
            (
                cast(user_correct_answers_query, Float)
                / cast(total_possible_correct_answers_query, Float)
                * 100
            ).label("accuracy_percentage")
        )

        result = await self.session.execute(query)
        accuracy_percentage = result.scalar()
        return accuracy_percentage

    async def total_average(self) -> float:
        total_possible_correct_answers_query = (
            select(func.count(answers_table.c.answer_id))
            .where(answers_table.c.is_correct.is_(True))
            .scalar_subquery()
        )

        total_user_correct_answers_query = select(
            func.sum(quiz_results_table.c.correct_answers)
        ).scalar_subquery()

        query = select(
            (
                cast(total_user_correct_answers_query, Float)
                / cast(total_possible_correct_answers_query, Float)
                * 100
            ).label("average_score_percentage")
        )

        result = await self.session.execute(query)
        average_score_percentage = result.scalar()

        return average_score_percentage

    async def get_overall_rating(self, user_id: UserId) -> Decimal:
        query = (
            select(
                func.avg(quiz_results_table.c.correct_answers).label(
                    "overall_rating"
                )
            )
            .select_from(
                quiz_results_table.join(
                    quiz_participations_table,
                    quiz_results_table.c.quiz_participation_id
                    == quiz_participations_table.c.quiz_participation_id,
                ).join(
                    company_users_table,
                    quiz_participations_table.c.company_user_id
                    == company_users_table.c.company_user_id,
                )
            )
            .where(company_users_table.c.user_id == user_id)
        )

        result = await self.session.execute(query)

        return result.scalar() if result else Decimal(0)

    async def get_user_quiz_averages(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime,
    ) -> list[QuizAverage]:
        query = (
            select(
                quiz_participations_table.c.quiz_id,
                func.avg(quiz_results_table.c.correct_answers).label(
                    "average_score"
                ),
            )
            .select_from(
                quiz_results_table.join(
                    quiz_participations_table,
                    quiz_results_table.c.quiz_participation_id
                    == quiz_participations_table.c.quiz_participation_id,
                ).join(
                    company_users_table,
                    quiz_participations_table.c.company_user_id
                    == company_users_table.c.company_user_id,
                )
            )
            .where(
                company_users_table.c.user_id == user_id,
                between(
                    quiz_participations_table.c.created_at,
                    start_date,
                    end_date,
                ),
            )
            .group_by(quiz_participations_table.c.quiz_id)
        )

        result = await self.session.execute(query)
        rows = result.fetchall()

        return [
            QuizAverage(quiz_id=row.quiz_id, average=float(row.average_score))
            for row in rows
        ]

    async def get_all_last_quiz_completion_times(
        self, user_id: UserId
    ) -> list[LastQuizCompletionTimes]:
        query = (
            select(
                quiz_participations_table.c.quiz_id,
                func.max(quiz_participations_table.c.created_at).label(
                    "last_completed"
                ),
            )
            .select_from(
                quiz_participations_table.join(
                    company_users_table,
                    quiz_participations_table.c.company_user_id
                    == company_users_table.c.company_user_id,
                )
            )
            .where(company_users_table.c.user_id == user_id)
            .group_by(quiz_participations_table.c.quiz_id)
        )

        result = await self.session.execute(query)
        rows = result.fetchall()

        return [
            LastQuizCompletionTimes(
                quiz_id=row.quiz_id, completion_data=row.last_completed
            )
            for row in rows
        ]

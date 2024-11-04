from dataclasses import dataclass

from app.core.common.pagination import Pagination
from app.core.interfaces.quiz_gateways import (
    QuizDetail,
    QuizFilters,
    QuizReader,
)


@dataclass(frozen=True)
class GetAllQuizzesInputData:
    filters: QuizFilters
    pagination: Pagination


@dataclass(frozen=True)
class GetAllQuizzesOutputData:
    total: int
    quizzes: list[QuizDetail]


@dataclass
class GetAllQuizzes:
    quiz_reader: QuizReader

    async def __call__(
        self, data: GetAllQuizzesInputData
    ) -> GetAllQuizzesOutputData:
        total = await self.quiz_reader.total(data.filters)
        quizzes = await self.quiz_reader.get_many(
            data.filters, data.pagination
        )

        return GetAllQuizzesOutputData(total, quizzes)

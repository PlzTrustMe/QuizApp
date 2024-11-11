from dataclasses import dataclass
from datetime import datetime

from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.quiz_gateways import (
    QuizAverage,
    QuizReader,
)


@dataclass(frozen=True)
class GetAllQuizAverageInputData:
    start_date: datetime
    end_date: datetime


@dataclass(frozen=True)
class GetAllQuizAverageOutputData:
    averages: list[QuizAverage]


@dataclass
class GetAllQuizAverage:
    id_provider: IdProvider
    quiz_gateway: QuizReader

    async def __call__(
        self, data: GetAllQuizAverageInputData
    ) -> GetAllQuizAverageOutputData:
        user = await self.id_provider.get_user()

        averages = await self.quiz_gateway.get_user_quiz_averages(
            user.user_id, data.start_date, data.end_date
        )

        return GetAllQuizAverageOutputData(averages)

from dataclasses import dataclass

from app.core.interfaces.quiz_gateways import QuizReader


@dataclass(frozen=True)
class GetTotalQuizAverageOutputData:
    average: float


@dataclass
class GetTotalQuizAverage:
    quiz_reader: QuizReader

    async def __call__(self) -> GetTotalQuizAverageOutputData:
        average = await self.quiz_reader.total_average()

        return GetTotalQuizAverageOutputData(average)

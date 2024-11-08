from dataclasses import dataclass

from app.core.interfaces.quiz_gateways import QuizReader


@dataclass(frozen=True)
class GetAllQuizAverageOutputData:
    average: float


@dataclass
class GetAllQuizAverage:
    quiz_reader: QuizReader

    async def __call__(self) -> GetAllQuizAverageOutputData:
        average = await self.quiz_reader.total_average()

        return GetAllQuizAverageOutputData(average)

from dataclasses import dataclass

from app.core.interfaces.quiz_gateways import QuizReader


@dataclass(frozen=True)
class GetAllQuizResultOutputData:
    average: float


@dataclass
class GetAllQuizResult:
    quiz_reader: QuizReader

    async def __call__(self) -> GetAllQuizResultOutputData:
        average = await self.quiz_reader.total_average()

        return GetAllQuizResultOutputData(average)

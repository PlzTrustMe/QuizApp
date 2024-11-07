from dataclasses import dataclass

from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.quiz_gateways import (
    LastQuizCompletionTimes,
    QuizReader,
)


@dataclass(frozen=True)
class GetLastCompletionTimesOutputData:
    quiz_completions: list[LastQuizCompletionTimes]


@dataclass
class GetLastCompletionTimes:
    id_provider: IdProvider
    quiz_reader: QuizReader

    async def __call__(self):
        user = await self.id_provider.get_user()

        quiz_completions = (
            await self.quiz_reader.get_all_last_quiz_completion_times(
                user.user_id
            )
        )

        return GetLastCompletionTimesOutputData(quiz_completions)

from dataclasses import dataclass

from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.quiz_gateways import QuizReader


@dataclass(frozen=True)
class GetMyOverallRatingOutputData:
    overall_rating: int


@dataclass
class GetMyOverallRating:
    id_provider: IdProvider
    quiz_reader: QuizReader

    async def __call__(self) -> GetMyOverallRatingOutputData:
        user = await self.id_provider.get_user()

        overall_rating = int(
            await self.quiz_reader.get_overall_rating(user.user_id)
        )

        return GetMyOverallRatingOutputData(overall_rating)

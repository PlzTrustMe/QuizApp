from dataclasses import dataclass

from app.core.commands.company.errors import CompanyUserNotFoundError
from app.core.commands.quiz.errors import (
    QuizParticipationNotFoundError,
)
from app.core.commands.user.errors import AccessDeniedError
from app.core.entities.quiz import QuizParticipationId
from app.core.interfaces.cache import CacheGateway
from app.core.interfaces.company_gateways import CompanyUserGateway
from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.quiz_gateways import (
    QuizParticipationGateway,
)
from app.utils.get_cache_key import get_quiz_result_cache_key


@dataclass(frozen=True)
class GetMyQuizResultInputData:
    participation_id: int


@dataclass(frozen=True)
class GetMyQuizResultOutputData:
    correct_answers: int | None


@dataclass
class GetMyQuizResult:
    id_provider: IdProvider
    quiz_participation_gateway: QuizParticipationGateway
    company_user_gateway: CompanyUserGateway
    cache: CacheGateway

    async def __call__(
        self, data: GetMyQuizResultInputData
    ) -> GetMyQuizResultOutputData:
        participation_id = QuizParticipationId(data.participation_id)

        participation = await self.quiz_participation_gateway.by_id(
            participation_id
        )
        if not participation:
            raise QuizParticipationNotFoundError(participation_id)

        actor = await self.id_provider.get_user()

        company_user = await self.company_user_gateway.by_id(
            participation.company_user_id
        )
        if not company_user:
            raise CompanyUserNotFoundError()

        if actor.user_id != company_user.user_id:
            raise AccessDeniedError()

        cache_key = get_quiz_result_cache_key(participation_id)

        cache_data = await self.cache.get_cache(cache_key)

        return (
            GetMyQuizResultOutputData(correct_answers=None)
            if not cache_data
            else GetMyQuizResultOutputData(
                correct_answers=cache_data["correct_answers"]
            )
        )

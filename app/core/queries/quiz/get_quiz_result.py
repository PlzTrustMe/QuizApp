from dataclasses import dataclass

from app.core.commands.company.errors import (
    CompanyNotFoundError,
    CompanyUserNotFoundError,
)
from app.core.commands.quiz.errors import (
    QuizParticipationNotFoundError,
)
from app.core.commands.user.errors import AccessDeniedError
from app.core.common.access_service import AccessService
from app.core.entities.quiz import QuizParticipationId
from app.core.interfaces.cache import CacheGateway
from app.core.interfaces.company_gateways import (
    CompanyGateway,
    CompanyUserGateway,
)
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
    access_service: AccessService
    quiz_participation_gateway: QuizParticipationGateway
    company_user_gateway: CompanyUserGateway
    company_gateway: CompanyGateway
    cache: CacheGateway

    async def by_user(
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

        return await self._get_data(participation_id)

    async def by_company(
        self, data: GetMyQuizResultInputData
    ) -> GetMyQuizResultOutputData:
        participation_id = QuizParticipationId(data.participation_id)

        participation = await self.quiz_participation_gateway.by_id(
            participation_id
        )
        if not participation:
            raise QuizParticipationNotFoundError(participation_id)

        company_user = await self.company_user_gateway.by_id(
            participation.company_user_id
        )
        if not company_user:
            raise CompanyUserNotFoundError()

        company = await self.company_gateway.by_id(company_user.company_id)
        if not company:
            raise CompanyNotFoundError(company_user.company_id)

        await self.access_service.ensure_can_get_quiz_result(company)

        return await self._get_data(participation_id)

    async def _get_data(
        self, participation_id: QuizParticipationId
    ) -> GetMyQuizResultOutputData:
        cache_key = get_quiz_result_cache_key(participation_id)

        cache_data = await self.cache.get_cache(cache_key)

        return (
            GetMyQuizResultOutputData(correct_answers=None)
            if not cache_data
            else GetMyQuizResultOutputData(
                correct_answers=cache_data["correct_answers"]
            )
        )

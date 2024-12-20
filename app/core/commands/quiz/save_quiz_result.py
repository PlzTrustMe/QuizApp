from dataclasses import asdict, dataclass

from app.core.commands.company.errors import CompanyUserNotFoundError
from app.core.commands.quiz.errors import (
    QuizNotFoundError,
    QuizParticipationNotFoundError,
)
from app.core.common.commiter import Commiter
from app.core.entities.company import CompanyId, CompanyUserId
from app.core.entities.quiz import (
    QuizId,
    QuizParticipationId,
    QuizResult,
    QuizResultId,
)
from app.core.interfaces.cache import CacheGateway
from app.core.interfaces.company_gateways import CompanyUserGateway
from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.quiz_gateways import (
    QuizGateway,
    QuizParticipationGateway,
    QuizResultGateway,
)
from app.utils.get_cache_key import get_member_key, get_quiz_result_cache_key


@dataclass(frozen=True)
class SaveQuizResultInputData:
    participation_id: int
    correct_answers: int


@dataclass
class SaveQuizResult:
    id_provider: IdProvider
    participation_gateway: QuizParticipationGateway
    quiz_gateway: QuizGateway
    company_user_gateway: CompanyUserGateway
    quiz_result_gateway: QuizResultGateway
    cache: CacheGateway
    commiter: Commiter

    async def __call__(self, data: SaveQuizResultInputData) -> QuizResultId:
        participation_id = QuizParticipationId(data.participation_id)

        user = await self.id_provider.get_user()

        quiz_participation = await self.participation_gateway.by_id(
            participation_id
        )
        if not quiz_participation:
            raise QuizParticipationNotFoundError(participation_id)

        quiz = await self.quiz_gateway.by_id(quiz_participation.quiz_id)
        if not quiz:
            raise QuizNotFoundError(quiz_participation.quiz_id)

        company_user = await self.company_user_gateway.by_company(
            quiz.company_id, user.user_id
        )
        if not company_user:
            raise CompanyUserNotFoundError()

        new_quiz_result = QuizResult(
            quiz_result_id=None,
            quiz_participation_id=participation_id,
            correct_answers=data.correct_answers,
        )

        await self.quiz_result_gateway.add(new_quiz_result)

        await self.commiter.commit()

        await self._set_cache(
            quiz_participation.quiz_participation_id,
            quiz.quiz_id,
            company_user.company_user_id,
            company_user.company_id,
            new_quiz_result,
        )

        return new_quiz_result.quiz_result_id

    async def _set_cache(
        self,
        participation_id: QuizParticipationId,
        quiz_id: QuizId,
        company_user_id: CompanyUserId,
        company_id: CompanyId,
        quiz_result: QuizResult,
    ) -> None:
        cache_data = {
            "participation_id": participation_id,
            "company_user_id": company_user_id,
            "company_id": company_id,
            "quiz_id": quiz_id,
        }

        cache_data.update(asdict(quiz_result))
        cache_key = get_quiz_result_cache_key(participation_id)
        member_key = get_member_key(company_id)

        ttl = 172800  # TTL in second(48 hours)

        await self.cache.set_cache(cache_key, cache_data, ttl)
        await self.cache.set_member_key(member_key, cache_key)

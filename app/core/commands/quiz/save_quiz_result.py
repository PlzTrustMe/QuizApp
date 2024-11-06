from dataclasses import dataclass

from app.core.commands.company.errors import CompanyUserNotFoundError
from app.core.commands.quiz.errors import (
    QuizNotFoundError,
    QuizParticipationNotFoundError,
)
from app.core.common.commiter import Commiter
from app.core.entities.quiz import (
    QuizParticipationId,
    QuizResult,
    QuizResultId,
)
from app.core.interfaces.company_gateways import CompanyUserGateway
from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.quiz_gateways import (
    QuizGateway,
    QuizParticipationGateway,
    QuizResultGateway,
)


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

        return new_quiz_result.quiz_result_id

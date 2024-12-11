from dataclasses import dataclass

from app.core.commands.company.errors import CompanyUserNotFoundError
from app.core.commands.quiz.errors import QuizNotFoundError
from app.core.common.commiter import Commiter
from app.core.entities.quiz import (
    QuizId,
    QuizParticipation,
    QuizParticipationId,
)
from app.core.interfaces.company_gateways import CompanyUserGateway
from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.quiz_gateways import (
    QuizGateway,
    QuizParticipationGateway,
)


@dataclass(frozen=True)
class TakeQuizInputData:
    quiz_id: int


@dataclass
class TakeQuiz:
    id_provider: IdProvider
    company_user_gateway: CompanyUserGateway
    quiz_gateway: QuizGateway
    participation_gateway: QuizParticipationGateway
    commiter: Commiter

    async def __call__(self, data: TakeQuizInputData) -> QuizParticipationId:
        quiz_id = QuizId(data.quiz_id)

        user = await self.id_provider.get_user()

        quiz = await self.quiz_gateway.by_id(quiz_id)
        if not quiz:
            raise QuizNotFoundError(quiz_id)

        company_user = await self.company_user_gateway.by_company(
            quiz.company_id, user.user_id
        )
        if not company_user:
            raise CompanyUserNotFoundError()

        new_quiz_participation = QuizParticipation(
            quiz_participation_id=None,
            quiz_id=quiz_id,
            company_user_id=company_user.company_user_id,
        )

        await self.participation_gateway.add(new_quiz_participation)

        await self.commiter.commit()

        return new_quiz_participation.quiz_participation_id

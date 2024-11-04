from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.commands.quiz.errors import QuizNotFoundError
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.quiz import QuizId
from app.core.interfaces.company_gateways import CompanyGateway
from app.core.interfaces.quiz_gateways import QuizGateway


@dataclass(frozen=True)
class EditQuizTitleInputData:
    quiz_id: int
    new_title: str


@dataclass
class EditQuizTitle:
    quiz_gateway: QuizGateway
    company_gateway: CompanyGateway
    access_service: AccessService
    commiter: Commiter

    async def __call__(self, data: EditQuizTitleInputData) -> None:
        quiz_id = QuizId(data.quiz_id)

        quiz = await self.quiz_gateway.by_id(quiz_id)
        if not quiz:
            raise QuizNotFoundError(quiz_id)

        company = await self.company_gateway.by_id(quiz.company_id)
        if not company:
            raise CompanyNotFoundError(quiz.company_id)

        await self.access_service.ensure_can_edit_quiz(company)

        quiz.title = data.new_title

        await self.commiter.commit()

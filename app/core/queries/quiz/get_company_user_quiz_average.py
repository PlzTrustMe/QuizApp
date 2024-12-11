from dataclasses import dataclass

from app.core.commands.company.errors import (
    CompanyNotFoundError,
    CompanyUserNotFoundError,
)
from app.core.common.access_service import AccessService
from app.core.entities.company import CompanyUserId
from app.core.interfaces.company_gateways import (
    CompanyGateway,
    CompanyUserGateway,
)
from app.core.interfaces.quiz_gateways import (
    AverageScore,
    QuizReader,
    TimeRange,
)


@dataclass(frozen=True)
class GetCompanyUserQuizAverageInputData:
    company_user_id: int
    time_range: TimeRange


@dataclass(frozen=True)
class GetCompanyUserQuizAverageOutputData:
    result: list[AverageScore]


@dataclass
class GetCompanyUserQuizAverage:
    company_user_gateway: CompanyUserGateway
    company_gateway: CompanyGateway
    access_service: AccessService
    quiz_reader: QuizReader

    async def __call__(self, data: GetCompanyUserQuizAverageInputData):
        company_user_id = CompanyUserId(data.company_user_id)

        company_user = await self.company_user_gateway.by_id(company_user_id)
        if not company_user:
            raise CompanyUserNotFoundError()

        company = await self.company_gateway.by_id(company_user.company_id)
        if not company:
            raise CompanyNotFoundError(company_user.company_id)

        await self.access_service.ensure_can_get_company_average_scores(
            company
        )

        result = await self.quiz_reader.get_company_user_quiz_average_scores(
            company_user_id, data.time_range
        )

        return GetCompanyUserQuizAverageOutputData(result)

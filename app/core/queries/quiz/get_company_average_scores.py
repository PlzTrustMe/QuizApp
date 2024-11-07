from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.common.access_service import AccessService
from app.core.entities.company import CompanyId
from app.core.interfaces.company_gateways import CompanyGateway
from app.core.interfaces.quiz_gateways import (
    CompanyAverageScore,
    QuizReader,
    TimeRange,
)


@dataclass(frozen=True)
class GetCompanyAverageScoresInputData:
    company_id: int
    time_range: TimeRange


@dataclass(frozen=True)
class GetCompanyAverageScoresOutputData:
    result: list[CompanyAverageScore]


@dataclass
class GetCompanyAverageScores:
    company_gateway: CompanyGateway
    access_service: AccessService
    quiz_reader: QuizReader

    async def __call__(self, data: GetCompanyAverageScoresInputData):
        company = await self.company_gateway.by_id(CompanyId(data.company_id))
        if not company:
            raise CompanyNotFoundError(data.company_id)

        await self.access_service.ensure_can_get_company_average_scores(
            company
        )

        result = await self.quiz_reader.get_company_average_scores_over_time(
            CompanyId(data.company_id), data.time_range.value
        )

        return GetCompanyAverageScoresOutputData(result=result)

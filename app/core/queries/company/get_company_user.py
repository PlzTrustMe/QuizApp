from dataclasses import dataclass

from app.core.commands.company.errors import CompanyUserNotFoundError
from app.core.entities.company import CompanyId, CompanyUserId
from app.core.interfaces.company_gateways import (
    CompanyUserDetail,
    CompanyUserReader,
)
from app.core.interfaces.quiz_gateways import QuizReader


@dataclass(frozen=True)
class GetCompanyUserInputData:
    company_user_id: int


@dataclass(frozen=True)
class GetCompanyOutputData:
    user_detail: CompanyUserDetail
    avg_score: float


@dataclass
class GetCompanyUser:
    company_user_reader: CompanyUserReader
    quiz_reader: QuizReader

    async def __call__(
        self, data: GetCompanyUserInputData
    ) -> GetCompanyOutputData:
        company_user_id = CompanyUserId(data.company_user_id)

        user_detail = await self.company_user_reader.by_id(company_user_id)
        if not user_detail:
            raise CompanyUserNotFoundError()

        avg_score = await self.quiz_reader.total_average_user_score(
            company_user_id, CompanyId(user_detail.company_id)
        )

        return GetCompanyOutputData(user_detail, avg_score)

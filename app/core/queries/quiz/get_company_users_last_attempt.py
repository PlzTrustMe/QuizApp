from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.common.access_service import AccessService
from app.core.entities.company import CompanyId
from app.core.interfaces.company_gateways import CompanyGateway
from app.core.interfaces.quiz_gateways import QuizReader, UserLastAttempt


@dataclass(frozen=True)
class GetCompanyUserLastAttemptInputData:
    company_id: int


@dataclass(frozen=True)
class GetCompanyUserLastAttemptOutputData:
    result: list[UserLastAttempt]


@dataclass
class GetCompanyUserLastAttempt:
    company_gateway: CompanyGateway
    access_service: AccessService
    quiz_reader: QuizReader

    async def __call__(
        self, data: GetCompanyUserLastAttemptInputData
    ) -> GetCompanyUserLastAttemptOutputData:
        company_id = CompanyId(data.company_id)

        company = await self.company_gateway.by_id(company_id)
        if not company:
            raise CompanyNotFoundError(company_id)

        await self.access_service._is_owner_or_admin(company)

        result = await self.quiz_reader.get_company_users_last_attempt(
            company_id
        )

        return GetCompanyUserLastAttemptOutputData(result)

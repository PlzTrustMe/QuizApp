from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.common.access_service import AccessService
from app.core.entities.company import CompanyId
from app.core.interfaces.cache import CacheGateway
from app.core.interfaces.company_gateways import CompanyGateway
from app.utils.get_cache_key import get_member_key


@dataclass(frozen=True)
class GetAllCompanyQuizResultInputData:
    company_id: int


@dataclass(frozen=True)
class QuizResult:
    participation_id: int
    correct_answers: int


@dataclass(frozen=True)
class GetAllCompanyQuizResultOutputData:
    results: list[QuizResult] | None


@dataclass
class GetAllCompanyQuizResult:
    company_gateway: CompanyGateway
    access_service: AccessService
    cache: CacheGateway

    async def __call__(self, data: GetAllCompanyQuizResultInputData):
        company = await self.company_gateway.by_id(CompanyId(data.company_id))
        if not company:
            raise CompanyNotFoundError(data.company_id)

        await self.access_service.ensure_can_get_quiz_result(company)

        member_key = get_member_key(company.company_id)
        participation_keys = await self.cache.get_member_data(member_key)

        results = [
            QuizResult(data["participation_id"], data["correct_answers"])
            for key in participation_keys
            if (data := await self.cache.get_cache(key))
        ]

        return GetAllCompanyQuizResultOutputData(results=results)

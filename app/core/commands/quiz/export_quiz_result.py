from dataclasses import dataclass
from enum import Enum

from app.core.commands.company.errors import (
    CompanyNotFoundError,
    CompanyUserNotFoundError,
)
from app.core.commands.quiz.errors import QuizParticipationNotFoundError
from app.core.common.access_service import AccessService
from app.core.common.export_data import (
    CSVExportStrategy,
    ExportContext,
    ExportStrategy,
    JSONExportStrategy,
)
from app.core.entities.quiz import QuizParticipationId
from app.core.interfaces.cache import CacheGateway
from app.core.interfaces.company_gateways import (
    CompanyGateway,
    CompanyUserGateway,
)
from app.core.interfaces.quiz_gateways import QuizParticipationGateway
from app.utils.get_cache_key import get_quiz_result_cache_key


class ExportFormat(str, Enum):
    CSV = "CSV"
    JSON = "JSON"


@dataclass(frozen=True)
class ExportQuizResultInputData:
    format: ExportFormat
    participation_id: int


@dataclass(frozen=True)
class ExportQuizResultOutputData:
    file_path: str
    media_type: str


@dataclass
class ExportQuizResult:
    access_service: AccessService
    quiz_participation_gateway: QuizParticipationGateway
    company_user_gateway: CompanyUserGateway
    company_gateway: CompanyGateway
    cache: CacheGateway

    async def __call__(
        self, data: ExportQuizResultInputData
    ) -> ExportQuizResultOutputData:
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

        cache_key = get_quiz_result_cache_key(participation_id)

        cache_data = await self.cache.get_cache(cache_key)

        export_context = ExportContext(self._set_strategy(data.format))

        file_path = export_context.export(participation_id, [cache_data])
        media_type = self._set_media_type(data.format)

        return ExportQuizResultOutputData(file_path, media_type)

    def _set_strategy(self, export_format: ExportFormat) -> ExportStrategy:
        if export_format == ExportFormat.CSV:
            return CSVExportStrategy()
        return JSONExportStrategy()

    def _set_media_type(self, export_format: ExportFormat) -> str:
        return (
            "text/csv" if format == export_format.CSV else "application/json"
        )

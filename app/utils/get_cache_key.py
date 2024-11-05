from app.core.entities.company import CompanyId
from app.core.entities.quiz import QuizParticipationId


def get_quiz_result_cache_key(participation_id: QuizParticipationId) -> str:
    return f"quiz_result:{participation_id}"


def get_member_key(company_id: CompanyId) -> str:
    return f"company:{company_id}"

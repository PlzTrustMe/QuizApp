from app.core.entities.quiz import QuizParticipationId


def get_quiz_result_cache_key(participation_id: QuizParticipationId) -> str:
    return f"quiz_result:{participation_id}"

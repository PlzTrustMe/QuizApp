from dataclasses import dataclass
from typing import NewType

from app.core.entities.company import CompanyId, CompanyUserId

QuizId = NewType("QuizId", int)
QuestionId = NewType("QuestionId", int)
AnswerId = NewType("AnswerId", int)
QuizParticipationId = NewType("QuizParticipationId", int)
QuizResultId = NewType("QuizResultId", int)


@dataclass
class Quiz:
    quiz_id: QuizId | None
    company_id: CompanyId
    title: str
    description: str
    participation_count: int = 0


@dataclass
class Question:
    question_id: QuestionId | None
    quiz_id: QuizId
    title: str


@dataclass
class Answer:
    answer_id: AnswerId | None
    question_id: QuestionId
    text: str
    is_correct: bool = False


@dataclass
class QuizParticipation:
    quiz_participation_id: QuizParticipationId | None
    quiz_id: QuizId
    company_user_id: CompanyUserId


@dataclass
class QuizResult:
    quiz_result_id: QuizResultId | None
    quiz_participation_id: QuizParticipationId
    correct_answers: int

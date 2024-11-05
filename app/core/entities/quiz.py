from dataclasses import dataclass
from typing import NewType

from app.core.entities.company import CompanyId

QuizId = NewType("QuizId", int)
QuestionId = NewType("QuestionId", int)
AnswerId = NewType("AnswerId", int)


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

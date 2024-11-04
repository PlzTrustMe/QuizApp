from abc import abstractmethod
from asyncio import Protocol
from dataclasses import dataclass

from app.core.common.pagination import Pagination
from app.core.entities.company import CompanyId, CompanyUserId
from app.core.entities.quiz import (
    Answer,
    Question,
    Quiz,
    QuizId,
    QuizParticipation,
    QuizParticipationId,
    QuizResult,
)


class QuizGateway(Protocol):
    @abstractmethod
    async def add(self, quiz: Quiz) -> None:
        raise NotImplementedError

    @abstractmethod
    async def by_id(self, quiz_id: QuizId) -> Quiz | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, quiz_id: QuizId) -> None:
        raise NotImplementedError


class QuizParticipationGateway(Protocol):
    @abstractmethod
    async def add(self, participation: QuizParticipation) -> None:
        raise NotImplementedError

    @abstractmethod
    async def by_id(
        self, quiz_participation_id: QuizParticipationId
    ) -> QuizParticipation | None:
        raise NotImplementedError


class QuizResultGateway(Protocol):
    @abstractmethod
    async def add(self, quiz_result: QuizResult) -> None:
        raise NotImplementedError


class QuestionGateway(Protocol):
    @abstractmethod
    async def add(self, question: Question) -> None:
        raise NotImplementedError


class AnswerGateway(Protocol):
    @abstractmethod
    async def add_many(self, answers: list[Answer]) -> None:
        raise NotImplementedError


@dataclass
class QuizFilters:
    company_id: int


@dataclass(frozen=True)
class AnswerDetail:
    answer_id: int
    text: str
    is_correct: bool


@dataclass(frozen=True)
class QuestionDetail:
    question_id: int
    title: str
    answers: list[AnswerDetail]


@dataclass(frozen=True)
class QuizDetail:
    quiz_id: int
    title: str
    description: str
    participation_count: int
    questions: list[QuestionDetail]


class QuizReader(Protocol):
    @abstractmethod
    async def get_many(
        self, filters: QuizFilters, pagination: Pagination
    ) -> list[QuizDetail]:
        raise NotImplementedError

    @abstractmethod
    async def total(self, filters: QuizFilters) -> int:
        raise NotImplementedError

    @abstractmethod
    async def total_average_user_score(
        self, company_user_id: CompanyUserId, company_id: CompanyId
    ) -> float:
        raise NotImplementedError

    @abstractmethod
    async def total_average(self) -> float:
        raise NotImplementedError

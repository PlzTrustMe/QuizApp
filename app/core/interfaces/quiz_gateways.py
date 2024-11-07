from abc import abstractmethod
from asyncio import Protocol
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum

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
from app.core.entities.user import UserId


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


@dataclass(frozen=True)
class QuizAverage:
    quiz_id: int
    average: float


@dataclass(frozen=True)
class LastQuizCompletionTimes:
    quiz_id: int
    completion_data: datetime


@dataclass(frozen=True)
class AverageScore:
    start_date: datetime
    average: Decimal


class TimeRange(str, Enum):
    YEAR = "year"
    MONTH = "month"
    WEEK = "week"


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

    @abstractmethod
    async def get_overall_rating(self, user_id: UserId) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_user_quiz_averages(
        self, user_id: UserId, start_data: datetime, end_data: datetime
    ) -> list[QuizAverage]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_last_quiz_completion_times(
        self, user_id: UserId
    ) -> list[LastQuizCompletionTimes]:
        raise NotImplementedError

    @abstractmethod
    async def get_company_average_scores_over_time(
        self, company_id: CompanyId, time_range: TimeRange
    ) -> list[AverageScore]:
        raise NotImplementedError

    @abstractmethod
    async def get_company_user_quiz_average_scores(
        self, company_user_id: CompanyUserId, time_range: TimeRange
    ) -> list[AverageScore]:
        raise NotImplementedError

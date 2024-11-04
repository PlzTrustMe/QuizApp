from abc import abstractmethod
from asyncio import Protocol

from app.core.entities.quiz import Answer, Question, Quiz, QuizId


class QuizGateway(Protocol):
    @abstractmethod
    async def add(self, quiz: Quiz) -> None:
        raise NotImplementedError

    @abstractmethod
    async def by_id(self, quiz_id: QuizId) -> Quiz | None:
        raise NotImplementedError


class QuestionGateway(Protocol):
    @abstractmethod
    async def add(self, question: Question) -> None:
        raise NotImplementedError


class AnswerGateway(Protocol):
    @abstractmethod
    async def add_many(self, answers: list[Answer]) -> None:
        raise NotImplementedError

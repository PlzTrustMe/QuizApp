from dataclasses import dataclass

from app.core.common.base_error import ApplicationError


@dataclass(eq=False)
class InvalidQuestionQuantityError(ApplicationError):
    @property
    def message(self) -> str:
        return "Each quiz must have at least two questions"


@dataclass(eq=False)
class InvalidAnswerQuantityError(ApplicationError):
    @property
    def message(self) -> str:
        return (
            "Each quiz must have at least two answers, but no "
            "more than four answers"
        )


@dataclass(eq=False)
class InvalidAnswersValidateError(ApplicationError):
    @property
    def message(self) -> str:
        return "There must be at least one correct answer per quiz"


@dataclass(eq=False)
class QuizNotFoundError(ApplicationError):
    quiz_id: int

    @property
    def message(self) -> str:
        return f"Quiz with id {self.quiz_id} not found"


@dataclass(eq=False)
class QuizParticipationNotFoundError(ApplicationError):
    participation_id: int

    @property
    def message(self) -> str:
        return f"Quiz participation with id {self.participation_id} not found"

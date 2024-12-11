from dataclasses import dataclass

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.common.access_service import AccessService
from app.core.common.commiter import Commiter
from app.core.entities.company import CompanyId
from app.core.entities.quiz import Answer, Question, Quiz, QuizId
from app.core.interfaces.company_gateways import CompanyGateway
from app.core.interfaces.quiz_gateways import (
    AnswerGateway,
    QuestionGateway,
    QuizGateway,
)
from app.core.interfaces.upload_file import UploadFile


@dataclass(frozen=True)
class UploadQuizzesInputData:
    company_id: int
    quiz_data: bytes


@dataclass
class UploadQuizzes:
    company_gateway: CompanyGateway
    access_service: AccessService
    uploader: UploadFile
    quiz_gateway: QuizGateway
    question_gateway: QuestionGateway
    answer_gateway: AnswerGateway
    commiter: Commiter

    async def __call__(self, data: UploadQuizzesInputData) -> None:
        company_id = CompanyId(data.company_id)

        company = await self.company_gateway.by_id(company_id)
        if not company:
            raise CompanyNotFoundError(company_id)

        await self.access_service.ensure_can_create_quiz(company)

        extract_quiz_data = self.uploader.upload_quiz(data.quiz_data)

        if len(extract_quiz_data) == 0:
            return

        for quiz_data in extract_quiz_data:
            quiz = await self.quiz_gateway.by_id(quiz_data["quiz_id"])

            if quiz:
                await self._update_quiz(quiz, quiz_data)
            else:
                await self._add_quiz(quiz_data, company_id)

        await self.commiter.commit()

    async def _update_quiz(self, quiz: Quiz, data: dict):
        quiz.title = data["title"]
        quiz.description = data["description"]

        await self._add_question_to_quiz(quiz.quiz_id, data["questions"])

    async def _add_quiz(self, data: dict, company_id: CompanyId):
        quiz = Quiz(
            quiz_id=None,
            title=data["title"],
            description=data["description"],
            company_id=company_id,
        )

        await self.quiz_gateway.add(quiz)
        await self._add_question_to_quiz(quiz.quiz_id, data["questions"])

    async def _add_question_to_quiz(
        self, quiz_id: QuizId, questions: list[dict]
    ):
        for question in questions:
            new_question = Question(
                question_id=None,
                quiz_id=quiz_id,
                title=question["title"],
            )

            await self.question_gateway.add(new_question)

            answers = [
                Answer(
                    answer_id=None,
                    question_id=new_question.question_id,
                    text=answer["text"],
                    is_correct=answer["is_correct"],
                )
                for answer in question["answers"]
            ]
            await self.answer_gateway.add_many(answers)

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from app.core.commands.quiz.create_quiz import (
    AnswerData,
    CreateQuiz,
    CreateQuizInputData,
    QuestionData,
)
from app.core.commands.quiz.delete_quiz import DeleteQuiz, DeleteQuizInputData
from app.core.commands.quiz.edit_quiz_title import (
    EditQuizTitle,
    EditQuizTitleInputData,
)
from app.core.entities.quiz import QuizId
from app.routers.responses.base import OkResponse
from app.schemas.quiz import CreateQuizSchema, EditQuizTitleSchema

quiz_router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
    route_class=DishkaRoute,
)


@quiz_router.post("", status_code=status.HTTP_201_CREATED)
async def create_new_quiz(
    body: CreateQuizSchema, action: FromDishka[CreateQuiz]
) -> OkResponse[QuizId]:
    question_data = [
        QuestionData(
            title=question.title,
            answers=[
                AnswerData(text=answer.text, is_correct=answer.is_correct)
                for answer in question.answers
            ],
        )
        for question in body.questions
    ]

    output_data = await action(
        CreateQuizInputData(
            company_id=body.company_id,
            title=body.title,
            description=body.description,
            questions=question_data,
        )
    )

    return OkResponse(status=201, result=output_data)


@quiz_router.put("/{quiz_id}/title", status_code=status.HTTP_200_OK)
async def edit_quiz_title(
    quiz_id: int, body: EditQuizTitleSchema, action: FromDishka[EditQuizTitle]
) -> OkResponse:
    await action(
        EditQuizTitleInputData(quiz_id=quiz_id, new_title=body.new_title)
    )

    return OkResponse()


@quiz_router.delete("/{quiz_id}", status_code=status.HTTP_200_OK)
async def delete_quiz(
    quiz_id: int, action: FromDishka[DeleteQuiz]
) -> OkResponse:
    await action(DeleteQuizInputData(quiz_id))

    return OkResponse()

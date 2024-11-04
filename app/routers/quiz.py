from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

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
from app.core.commands.quiz.save_quiz_result import (
    SaveQuizResult,
    SaveQuizResultInputData,
)
from app.core.commands.quiz.take_quiz import TakeQuiz, TakeQuizInputData
from app.core.common.pagination import Pagination, SortOrder
from app.core.entities.quiz import QuizId, QuizParticipationId, QuizResultId
from app.core.interfaces.quiz_gateways import QuizFilters
from app.core.queries.quiz.get_all_quiz_result import (
    GetAllQuizResult,
    GetAllQuizResultOutputData,
)
from app.core.queries.quiz.get_quizzes import (
    GetAllQuizzes,
    GetAllQuizzesInputData,
    GetAllQuizzesOutputData,
)
from app.routers.responses.base import OkResponse
from app.schemas.quiz import (
    CreateQuizSchema,
    EditQuizTitleSchema,
    SaveQuizResultSchema,
    TakeQuizSchema,
)

quiz_router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
    route_class=DishkaRoute,
)


@quiz_router.get("/average")
async def get_all_quizzes_average(
    action: FromDishka[GetAllQuizResult],
) -> OkResponse[GetAllQuizResultOutputData]:
    output_data = await action()

    return OkResponse(result=output_data)


@quiz_router.get("/{company_id}", status_code=status.HTTP_200_OK)
async def get_all_quizzes(
    action: FromDishka[GetAllQuizzes],
    company_id: int,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
) -> OkResponse[GetAllQuizzesOutputData]:
    output_data = await action(
        GetAllQuizzesInputData(
            QuizFilters(company_id), Pagination(offset, limit, order)
        )
    )

    return OkResponse(result=output_data)


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


@quiz_router.post("/take", status_code=status.HTTP_201_CREATED)
async def take_quiz(
    body: TakeQuizSchema, action: FromDishka[TakeQuiz]
) -> OkResponse[QuizParticipationId]:
    output_data = await action(TakeQuizInputData(quiz_id=body.quiz_id))

    return OkResponse(status=201, result=output_data)


@quiz_router.post("/save-result", status_code=status.HTTP_201_CREATED)
async def save_quiz_result(
    body: SaveQuizResultSchema, action: FromDishka[SaveQuizResult]
) -> OkResponse[QuizResultId]:
    output_data = await action(
        SaveQuizResultInputData(
            participation_id=body.participation_id,
            correct_answers=body.correct_answers,
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
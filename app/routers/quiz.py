import os.path
from datetime import datetime
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status
from fastapi.responses import FileResponse

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
from app.core.commands.quiz.export_quiz_result import (
    ExportFormat,
    ExportQuizResult,
    ExportQuizResultInputData,
)
from app.core.commands.quiz.save_quiz_result import (
    SaveQuizResult,
    SaveQuizResultInputData,
)
from app.core.commands.quiz.take_quiz import TakeQuiz, TakeQuizInputData
from app.core.common.pagination import Pagination, SortOrder
from app.core.entities.quiz import QuizId, QuizParticipationId, QuizResultId
from app.core.interfaces.quiz_gateways import QuizFilters, TimeRange
from app.core.queries.quiz.get_all_company_quiz_result import (
    GetAllCompanyQuizResult,
    GetAllCompanyQuizResultInputData,
    GetAllCompanyQuizResultOutputData,
)
from app.core.queries.quiz.get_all_last_quiz_completion_times import (
    GetLastCompletionTimes,
    GetLastCompletionTimesOutputData,
)
from app.core.queries.quiz.get_all_quiz_average import (
    GetAllQuizAverage,
    GetAllQuizAverageInputData,
    GetAllQuizAverageOutputData,
)
from app.core.queries.quiz.get_company_average_scores import (
    GetCompanyAverageScores,
    GetCompanyAverageScoresInputData,
    GetCompanyAverageScoresOutputData,
)
from app.core.queries.quiz.get_company_user_quiz_average import (
    GetCompanyUserQuizAverage,
    GetCompanyUserQuizAverageInputData,
    GetCompanyUserQuizAverageOutputData,
)
from app.core.queries.quiz.get_my_overall_rating import (
    GetMyOverallRating,
    GetMyOverallRatingOutputData,
)
from app.core.queries.quiz.get_quiz_result import (
    GetQuizResult,
    GetQuizResultInputData,
    GetQuizResultOutputData,
)
from app.core.queries.quiz.get_quizzes import (
    GetAllQuizzes,
    GetAllQuizzesInputData,
    GetAllQuizzesOutputData,
)
from app.core.queries.quiz.get_total_quiz_average import (
    GetTotalQuizAverage,
    GetTotalQuizAverageOutputData,
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


@quiz_router.get("/export/{participation_id}")
async def export_quiz_result(
    participation_id: int,
    action: FromDishka[ExportQuizResult],
    export_format: ExportFormat | None = None,
):
    output_data = await action(
        ExportQuizResultInputData(
            format=export_format, participation_id=participation_id
        )
    )

    return FileResponse(
        output_data.file_path,
        media_type=output_data.media_type,
        filename=os.path.basename(output_data.file_path),  # noqa: PTH119
    )


@quiz_router.get("/last-completion", status_code=status.HTTP_200_OK)
async def get_all_last_quiz_completion_times(
    action: FromDishka[GetLastCompletionTimes],
) -> OkResponse[GetLastCompletionTimesOutputData]:
    output_data = await action()

    return OkResponse(result=output_data)


@quiz_router.get(
    "/company-average-score/{company_id}", status_code=status.HTTP_200_OK
)
async def get_company_average_score(
    company_id: int,
    time_range: TimeRange,
    action: FromDishka[GetCompanyAverageScores],
) -> OkResponse[GetCompanyAverageScoresOutputData]:
    output_data = await action(
        GetCompanyAverageScoresInputData(company_id, time_range)
    )

    return OkResponse(result=output_data)


@quiz_router.get(
    "/company-user-average-score/{company_user_id}",
    status_code=status.HTTP_200_OK,
)
async def get_company_user_quiz_average(
    company_user_id: int,
    time_range: TimeRange,
    action: FromDishka[GetCompanyUserQuizAverage],
) -> OkResponse[GetCompanyUserQuizAverageOutputData]:
    output_data = await action(
        GetCompanyUserQuizAverageInputData(company_user_id, time_range)
    )

    return OkResponse(result=output_data)


@quiz_router.get("/average", status_code=status.HTTP_200_OK)
async def get_total_quizzes_average(
    action: FromDishka[GetTotalQuizAverage],
) -> OkResponse[GetTotalQuizAverageOutputData]:
    output_data = await action()

    return OkResponse(result=output_data)


@quiz_router.get("/all/average", status_code=status.HTTP_200_OK)
async def get_all_quizzes_average(
    action: FromDishka[GetAllQuizAverage],
    start_data: datetime,
    end_data: datetime,
) -> OkResponse[GetAllQuizAverageOutputData]:
    output_data = await action(
        GetAllQuizAverageInputData(start_data, end_data)
    )

    return OkResponse(result=output_data)


@quiz_router.get("/my/overall-rating", status_code=status.HTTP_200_OK)
async def get_my_overall_rating(
    action: FromDishka[GetMyOverallRating],
) -> OkResponse[GetMyOverallRatingOutputData]:
    output_data = await action()

    return OkResponse(result=output_data)


@quiz_router.get("/my/{participation_id}", status_code=status.HTTP_200_OK)
async def get_my_quiz_result(
    participation_id: int, action: FromDishka[GetQuizResult]
) -> OkResponse[GetQuizResultOutputData]:
    output_data = await action.by_user(
        GetQuizResultInputData(participation_id)
    )

    return OkResponse(result=output_data)


@quiz_router.get("/company/{participation_id}", status_code=status.HTTP_200_OK)
async def get_company_user_quiz_result(
    participation_id: int, action: FromDishka[GetQuizResult]
) -> OkResponse[GetQuizResultOutputData]:
    output_data = await action.by_company(
        GetQuizResultInputData(participation_id)
    )

    return OkResponse(result=output_data)


@quiz_router.get("/company/all/{company_id}", status_code=status.HTTP_200_OK)
async def get_all_company_quiz_results(
    company_id: int, action: FromDishka[GetAllCompanyQuizResult]
) -> OkResponse[GetAllCompanyQuizResultOutputData]:
    output_data = await action(GetAllCompanyQuizResultInputData(company_id))

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

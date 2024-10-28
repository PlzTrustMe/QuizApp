from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from app.core.commands.company.create_company import (
    CreateCompany,
    CreateCompanyInputData,
)
from app.core.commands.company.errors import CompanyWithNameAlreadyExistError
from app.core.entities.company import CompanyId
from app.core.entities.errors import (
    CompanyDescriptionTooLongError,
    CompanyNameTooLongError,
    EmptyError,
)
from app.routers.responses.base import ErrorResponse, OkResponse
from app.schemas.company import CreateCompanySchema

company_router = APIRouter(
    prefix="/company",
    tags=["Company"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
    route_class=DishkaRoute,
)


@company_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": CompanyId},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[
                CompanyNameTooLongError
                | CompanyDescriptionTooLongError
                | EmptyError
            ]
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse[CompanyWithNameAlreadyExistError]
        },
    },
)
async def create_new_company(
    body: CreateCompanySchema, action: FromDishka[CreateCompany]
) -> OkResponse[CompanyId]:
    response = await action(
        CreateCompanyInputData(name=body.name, description=body.description)
    )

    return OkResponse(status=201, result=response)

from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

from app.core.commands.company.create_company import (
    CreateCompany,
    CreateCompanyInputData,
)
from app.core.commands.company.delete_company import (
    DeleteCompany,
    DeleteCompanyInputData,
)
from app.core.commands.company.edit_company_description import (
    EditCompanyDescription,
    EditCompanyDescriptionInputData,
)
from app.core.commands.company.edit_company_name import (
    EditCompanyName,
    EditCompanyNameInputData,
)
from app.core.commands.company.edit_company_visibility import (
    EditCompanyVisibility,
    EditCompanyVisibilityInputData,
)
from app.core.commands.company.errors import (
    CompanyNotFoundError,
    CompanyWithNameAlreadyExistError,
)
from app.core.commands.company.leave_from_company import (
    LeaveFromCompany,
    LeaveFromCompanyInputData,
)
from app.core.commands.company.remove_user_from_company import (
    RemoveUserFromCompany,
    RemoveUserFromCompanyInputData,
)
from app.core.commands.user.errors import AccessDeniedError, UnauthorizedError
from app.core.common.pagination import Pagination, SortOrder
from app.core.entities.company import CompanyId, CompanyRole, Visibility
from app.core.entities.errors import (
    CompanyDescriptionTooLongError,
    CompanyNameTooLongError,
    EmptyError,
)
from app.core.interfaces.company_gateways import (
    CompanyDetail,
    CompanyFilters,
    CompanyUserFilters,
)
from app.core.queries.company.get_company_by_id import (
    GetCompanyById,
    GetCompanyByIdInputData,
)
from app.core.queries.company.get_company_user import (
    GetCompanyOutputData,
    GetCompanyUser,
    GetCompanyUserInputData,
)
from app.core.queries.company.get_company_users import (
    GetCompanyUsers,
    GetCompanyUsersInputData,
    GetCompanyUsersOutputData,
)
from app.core.queries.company.get_many_companies import (
    GetManyCompanies,
    GetManyCompaniesInputData,
)
from app.routers.responses.base import ErrorResponse, OkResponse
from app.schemas.company import (
    CreateCompanySchema,
    EditCompanyDescriptionSchema,
    EditCompanyNameSchema,
    EditCompanyVisibilitySchema,
)

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


@company_router.get(
    "/{company_id}",
    responses={
        status.HTTP_200_OK: {"model": CompanyDetail},
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[CompanyNotFoundError]
        },
    },
)
async def get_company_by_id(
    company_id: int, action: FromDishka[GetCompanyById]
) -> OkResponse[CompanyDetail]:
    response = await action(GetCompanyByIdInputData(company_id))

    return OkResponse(result=response)


@company_router.get(
    "", responses={status.HTTP_200_OK: {"model": list[CompanyDetail]}}
)
async def get_many_companies(
    action: FromDishka[GetManyCompanies],
    visibility: Visibility | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
):
    response = await action(
        GetManyCompaniesInputData(
            filters=CompanyFilters(visibility=visibility),
            pagination=Pagination(offset, limit, order),
        )
    )

    return OkResponse(result=response)


@company_router.get("/users/{company_id}")
async def get_company_users(
    action: FromDishka[GetCompanyUsers],
    company_id: int,
    company_role: CompanyRole | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
) -> OkResponse[GetCompanyUsersOutputData]:
    response = await action(
        GetCompanyUsersInputData(
            filters=CompanyUserFilters(
                company_id=company_id, company_role=company_role
            ),
            pagination=Pagination(offset, limit, order),
        )
    )

    return OkResponse(result=response)


@company_router.get("/user/{company_user_id}")
async def get_company_user(
    company_user_id: int, action: FromDishka[GetCompanyUser]
) -> OkResponse[GetCompanyOutputData]:
    output_data = await action(GetCompanyUserInputData(company_user_id))

    return OkResponse(result=output_data)


@company_router.put(
    "/{company_id}/name",
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse[UnauthorizedError]
        },
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse[AccessDeniedError]},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[EmptyError | CompanyNameTooLongError]
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[CompanyNotFoundError]
        },
    },
)
async def edit_company_name(
    company_id: int,
    body: EditCompanyNameSchema,
    action: FromDishka[EditCompanyName],
) -> OkResponse:
    await action(
        EditCompanyNameInputData(company_id=company_id, name=body.new_name)
    )

    return OkResponse()


@company_router.put(
    "/{company_id}/description",
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse[UnauthorizedError]
        },
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse[AccessDeniedError]},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[CompanyDescriptionTooLongError]
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[CompanyNotFoundError]
        },
    },
)
async def edit_company_description(
    company_id: int,
    body: EditCompanyDescriptionSchema,
    action: FromDishka[EditCompanyDescription],
) -> OkResponse:
    await action(
        EditCompanyDescriptionInputData(
            company_id=company_id, description=body.new_description
        )
    )

    return OkResponse()


@company_router.put(
    "/{company_id}/visibility",
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse[UnauthorizedError]
        },
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse[AccessDeniedError]},
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[CompanyNotFoundError]
        },
    },
)
async def edit_company_visibility(
    company_id: int,
    body: EditCompanyVisibilitySchema,
    action: FromDishka[EditCompanyVisibility],
) -> OkResponse:
    await action(
        EditCompanyVisibilityInputData(
            company_id=company_id, visibility=body.visibility
        )
    )

    return OkResponse()


@company_router.delete(
    "/{company_id}",
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse[UnauthorizedError]
        },
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse[AccessDeniedError]},
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse[CompanyNotFoundError]
        },
    },
)
async def delete_company(
    company_id: int, action: FromDishka[DeleteCompany]
) -> OkResponse:
    await action(DeleteCompanyInputData(company_id))

    return OkResponse()


@company_router.delete("/remove-user/{company_id}/{user_id}")
async def remove_user_from_company(
    company_id: int, user_id: int, action: FromDishka[RemoveUserFromCompany]
) -> OkResponse:
    await action(
        RemoveUserFromCompanyInputData(company_id=company_id, user_id=user_id)
    )

    return OkResponse()


@company_router.delete("/leave/{company_id}")
async def leave_from_company(
    company_id: int, action: FromDishka[LeaveFromCompany]
):
    await action(LeaveFromCompanyInputData(company_id=company_id))

from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, Query, status

from app.core.commands.add_user import (
    SignUp,
    SignUpInputData,
    SignUpOutputData,
)
from app.core.commands.delete_user import DeleteUser, DeleteUserInputData
from app.core.commands.edit_full_name import (
    EditFullName,
    EditFullNameInputData,
    EditFullNameOutputData,
)
from app.core.common.base_error import ApplicationError
from app.core.common.pagination import Pagination, SortOrder
from app.core.interfaces.user_gateways import UserDetail, UserFilters
from app.core.queries.get_user import GetUserById, GetUserByIdInputData
from app.core.queries.get_users import (
    GetUsers,
    GetUsersInputData,
    GetUsersOutputData,
)
from app.schemas.base import ErrorSchema
from app.schemas.user import SignUpSchema, UserUpdateFullNameSchema

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
    route_class=DishkaRoute,
)


@user_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": SignUpOutputData},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def sign_up(body: SignUpSchema, action: FromDishka[SignUp]):
    try:
        response = await action(
            SignUpInputData(
                email=body.email,
                password=body.password,
                first_name=body.first_name,
                last_name=body.last_name,
            )
        )
    except ApplicationError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": error.message},
        ) from error
    else:
        return response


@user_router.put(
    "/{user_id}/full_name",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": EditFullNameOutputData},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def edit_full_name(
    user_id: int,
    body: UserUpdateFullNameSchema,
    action: FromDishka[EditFullName],
):
    try:
        response = await action(
            EditFullNameInputData(
                user_id=user_id,
                first_name=body.first_name,
                last_name=body.last_name,
            )
        )
    except ApplicationError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": error.message},
        ) from error
    else:
        return response


@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, action: FromDishka[DeleteUser]):
    try:
        await action(
            DeleteUserInputData(
                user_id=user_id,
            )
        )
    except ApplicationError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": error.message},
        ) from error


@user_router.get(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {"model": UserDetail},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def get_user(user_id: int, action: FromDishka[GetUserById]):
    try:
        response = await action(GetUserByIdInputData(user_id=user_id))
    except ApplicationError as error:
        raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail={"error": error.message},
        ) from error
    else:
        return response


@user_router.get("", response_model=GetUsersOutputData)
async def get_users(
    action: FromDishka[GetUsers],
    is_active: bool | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
):
    response = await action(
        GetUsersInputData(
            filters=UserFilters(is_active=is_active),
            pagination=Pagination(offset=offset, limit=limit, order=order),
        )
    )

    return response

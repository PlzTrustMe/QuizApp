from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Query, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

from app.core.commands.delete_user import DeleteUser, DeleteUserInputData
from app.core.commands.edit_full_name import (
    EditFullName,
    EditFullNameInputData,
    EditFullNameOutputData,
)
from app.core.commands.edit_password import EditPassword, EditPasswordInputData
from app.core.commands.errors import (
    AccessDeniedError,
    AccessTokenIsExpiredError,
    PasswordMismatchError,
    UnauthorizedError,
    UserNotFoundError,
)
from app.core.commands.sign_in import SignIn, SignInInputData
from app.core.commands.sign_in_by_oauth import (
    SignInByOauth,
    SignInByOauthInputData,
)
from app.core.commands.sign_up import (
    SignUp,
    SignUpInputData,
    SignUpOutputData,
)
from app.core.common.pagination import Pagination, SortOrder
from app.core.entities.errors import (
    EmptyError,
    FirstNameTooLongError,
    InvalidUserEmailError,
    LastNameTooLongError,
    WeakPasswordError,
)
from app.core.interfaces.user_gateways import UserDetail, UserFilters
from app.core.queries.get_me import GetMe
from app.core.queries.get_user import GetUserById, GetUserByIdInputData
from app.core.queries.get_users import (
    GetUsers,
    GetUsersInputData,
    GetUsersOutputData,
)
from app.routers.auth.token_auth import TokenAuth
from app.routers.responses.base import ErrorResponse, OkResponse
from app.schemas.user import (
    SignInSchema,
    SignUpSchema,
    UserUpdateFullNameSchema,
    UserUpdatePassword,
)

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
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[
                FirstNameTooLongError | LastNameTooLongError | EmptyError
            ]
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse[InvalidUserEmailError | WeakPasswordError]
        },
    },
)
async def sign_up(
    body: SignUpSchema, action: FromDishka[SignUp]
) -> OkResponse[SignUpOutputData]:
    response = await action(
        SignUpInputData(
            email=body.email,
            password=body.password,
            first_name=body.first_name,
            last_name=body.last_name,
        )
    )

    return OkResponse(result=response)


@user_router.post(
    "/sign-in",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": {}},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse[InvalidUserEmailError]
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse[PasswordMismatchError | UnauthorizedError]
        },
    },
)
async def sign_in(
    body: SignInSchema,
    action: FromDishka[SignIn],
    token_auth: FromDishka[TokenAuth],
) -> Response:
    access_token_data = await action(
        SignInInputData(email=body.email, password=body.password)
    )

    response = JSONResponse(status_code=200, content={})

    return token_auth.set_session(access_token_data, response)


@user_router.post(
    "/sign-in/oauth",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": {}},
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse[UnauthorizedError]
        },
    },
)
async def sing_in_by_auth0(
    create_new_user: FromDishka[SignInByOauth],
    token_auth: FromDishka[TokenAuth],
    token: str = Depends(HTTPBearer()),
):
    access_token_data = token_auth.get_token_data(token.credentials)

    await create_new_user(SignInByOauthInputData(access_token_data.email))

    response = JSONResponse(status_code=200, content={})

    return token_auth.set_session(access_token_data, response)


@user_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": UserDetail},
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse[
                UnauthorizedError | AccessTokenIsExpiredError
            ]
        },
    },
)
async def get_me(action: FromDishka[GetMe]) -> OkResponse[UserDetail]:
    response = await action()

    return OkResponse(result=response)


@user_router.put(
    "/{user_id}/full_name",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": EditFullNameOutputData},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[UserNotFoundError]},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[
                FirstNameTooLongError | LastNameTooLongError | EmptyError
            ]
        },
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse[AccessDeniedError]},
    },
)
async def edit_full_name(
    user_id: int,
    body: UserUpdateFullNameSchema,
    action: FromDishka[EditFullName],
) -> OkResponse[EditFullNameOutputData]:
    response = await action(
        EditFullNameInputData(
            user_id=user_id,
            first_name=body.first_name,
            last_name=body.last_name,
        )
    )

    return OkResponse(result=response)


@user_router.put(
    "/{user_id}/password",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[UserNotFoundError]},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[PasswordMismatchError]
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse[WeakPasswordError]
        },
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse[AccessDeniedError]},
    },
)
async def edit_password(
    user_id: int, body: UserUpdatePassword, action: FromDishka[EditPassword]
) -> OkResponse:
    await action(
        EditPasswordInputData(
            user_id=user_id,
            old_password=body.old_password,
            new_password=body.new_password,
        )
    )

    return OkResponse()


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[UserNotFoundError]},
    },
)
async def delete_user(
    user_id: int, action: FromDishka[DeleteUser]
) -> OkResponse:
    await action(
        DeleteUserInputData(
            user_id=user_id,
        )
    )

    return OkResponse()


@user_router.get(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {"model": UserDetail},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[UserNotFoundError]},
    },
)
async def get_user(
    user_id: int, action: FromDishka[GetUserById]
) -> OkResponse[UserDetail]:
    response = await action(GetUserByIdInputData(user_id=user_id))

    return OkResponse(result=response)


@user_router.get("")
async def get_users(
    action: FromDishka[GetUsers],
    is_active: bool | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
) -> OkResponse[GetUsersOutputData]:
    response = await action(
        GetUsersInputData(
            filters=UserFilters(is_active=is_active),
            pagination=Pagination(offset=offset, limit=limit, order=order),
        )
    )

    return OkResponse(result=response)

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status

from app.core.commands.add_user import (
    SignUp,
    SignUpInputData,
    SignUpOutputData,
)
from app.core.common.base_error import ApplicationError
from app.schemas.base import ErrorSchema
from app.schemas.user import SignUpSchema

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
    route_class=DishkaRoute,
)


@user_router.post(
    "/",
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

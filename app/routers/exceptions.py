import logging
from functools import partial
from typing import Awaitable, Callable

from fastapi import FastAPI, status
from starlette.requests import Request

from app.core.commands.company.errors import (
    CompanyNotFoundError,
    CompanyWithNameAlreadyExistError,
)
from app.core.commands.user.errors import (
    AccessDeniedError,
    AccessTokenIsExpiredError,
    PasswordMismatchError,
    UnauthorizedError,
    UserEmailAlreadyExistError,
    UserNotFoundError,
)
from app.core.common.base_error import ApplicationError
from app.core.entities.errors import (
    CompanyDescriptionTooLongError,
    CompanyNameTooLongError,
    EmptyError,
    FirstNameTooLongError,
    InvalidUserEmailError,
    LastNameTooLongError,
    WeakPasswordError,
)
from app.routers.responses.base import ErrorData, ErrorResponse
from app.routers.responses.orjson import ORJSONResponse

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationError, error_handler(500))
    app.add_exception_handler(
        FirstNameTooLongError, error_handler(status.HTTP_400_BAD_REQUEST)
    )
    app.add_exception_handler(
        CompanyNameTooLongError, error_handler(status.HTTP_400_BAD_REQUEST)
    )
    app.add_exception_handler(
        CompanyDescriptionTooLongError,
        error_handler(status.HTTP_400_BAD_REQUEST),
    )
    app.add_exception_handler(
        LastNameTooLongError, error_handler(status.HTTP_400_BAD_REQUEST)
    )
    app.add_exception_handler(
        EmptyError, error_handler(status.HTTP_400_BAD_REQUEST)
    )
    app.add_exception_handler(
        InvalidUserEmailError,
        error_handler(status.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(
        WeakPasswordError, error_handler(status.HTTP_422_UNPROCESSABLE_ENTITY)
    )
    app.add_exception_handler(
        UserNotFoundError, error_handler(status.HTTP_404_NOT_FOUND)
    )
    app.add_exception_handler(
        CompanyNotFoundError, error_handler(status.HTTP_404_NOT_FOUND)
    )
    app.add_exception_handler(
        UserEmailAlreadyExistError, error_handler(status.HTTP_409_CONFLICT)
    )
    app.add_exception_handler(
        CompanyWithNameAlreadyExistError,
        error_handler(status.HTTP_409_CONFLICT),
    )
    app.add_exception_handler(
        PasswordMismatchError, error_handler(status.HTTP_401_UNAUTHORIZED)
    )
    app.add_exception_handler(
        UnauthorizedError, error_handler(status.HTTP_401_UNAUTHORIZED)
    )
    app.add_exception_handler(
        AccessTokenIsExpiredError, error_handler(status.HTTP_401_UNAUTHORIZED)
    )
    app.add_exception_handler(
        AccessDeniedError, error_handler(status.HTTP_403_FORBIDDEN)
    )
    app.add_exception_handler(Exception, unknown_exception_handler)


def error_handler(
    status_code: int,
) -> Callable[..., Awaitable[ORJSONResponse]]:
    return partial(app_error_handler, status_code=status_code)


async def app_error_handler(
    request: Request, err: ApplicationError, status_code: int
) -> ORJSONResponse:
    return await handle_error(
        request=request,
        err=err,
        err_data=ErrorData(message=err.message, data=err),
        status=500,
        status_code=status_code,
    )


async def unknown_exception_handler(
    request: Request, err: Exception
) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception(
        "Unknown error occurred", exc_info=err, extra={"error": err}
    )
    return ORJSONResponse(
        ErrorResponse(error=ErrorData(data=err)),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_error(
    request: Request,
    err: Exception,
    err_data: ErrorData,
    status: int,
    status_code: int,
) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err)
    return ORJSONResponse(
        ErrorResponse(error=err_data, status=status_code),
        status_code=status_code,
    )

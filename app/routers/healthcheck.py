from dataclasses import dataclass

from fastapi import APIRouter, status

healthcheck_router = APIRouter(tags=["Healthcheck"])


@dataclass(frozen=True)
class OkStatus:
    status_code: int = 200
    detail: str = "ok"
    result: str = "working"


OK_STATUS = OkStatus()


@healthcheck_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Healthcheck endpoint to check the health of the project",
)
async def healthcheck_handler() -> OkStatus:
    return OK_STATUS

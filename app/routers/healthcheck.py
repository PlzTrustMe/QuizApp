from fastapi import APIRouter, status

from app.schemas.healthckech import HealthCheckResponseSchema

healthcheck_router = APIRouter(tags=["Healthcheck"])


@healthcheck_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Healthcheck endpoint to check the health of the project",
    responses={
        status.HTTP_200_OK: {"model": HealthCheckResponseSchema}
    }
)
async def healthcheck_handler() -> HealthCheckResponseSchema:
    return HealthCheckResponseSchema()

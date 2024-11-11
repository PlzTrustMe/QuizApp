from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

from app.core.commands.notification.mark_read_notification import (
    MarkReadNotification,
    MarkReadNotificationInputData,
)
from app.core.common.pagination import Pagination, SortOrder
from app.core.entities.notification import NotificationStatus
from app.core.queries.notification.get_my_notifications import (
    GetMyNotifications,
    GetMyNotificationsInputData,
    GetMyNotificationsOutputData,
)
from app.routers.responses.base import OkResponse

notification_router = APIRouter(
    prefix="/notification",
    tags=["Notification"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
    route_class=DishkaRoute,
)


@notification_router.get("/my/{company_id}", status_code=status.HTTP_200_OK)
async def get_my_notifications(
    company_id: int,
    action: FromDishka[GetMyNotifications],
    notification_status: NotificationStatus | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
) -> OkResponse[GetMyNotificationsOutputData]:
    output_data = await action(
        GetMyNotificationsInputData(
            company_id=company_id,
            status=notification_status,
            pagination=Pagination(offset, limit, order),
        )
    )

    return OkResponse(result=output_data)


@notification_router.put(
    "/{notification_id}/status", status_code=status.HTTP_200_OK
)
async def mark_read_notification(
    notification_id: int, action: FromDishka[MarkReadNotification]
) -> OkResponse:
    await action(MarkReadNotificationInputData(notification_id))

    return OkResponse()

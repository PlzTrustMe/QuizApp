from dataclasses import dataclass

from app.core.commands.company.errors import CompanyUserNotFoundError
from app.core.common.pagination import Pagination
from app.core.entities.company import CompanyId
from app.core.entities.notification import NotificationStatus
from app.core.interfaces.company_gateways import (
    CompanyUserGateway,
)
from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.notification_gateways import (
    NotificationDetail,
    NotificationFilters,
    NotificationReader,
)


@dataclass(frozen=True)
class GetMyNotificationsInputData:
    company_id: int
    status: NotificationStatus | None
    pagination: Pagination


@dataclass(frozen=True)
class GetMyNotificationsOutputData:
    notifications: list[NotificationDetail]


@dataclass
class GetMyNotifications:
    id_provider: IdProvider
    company_user_gateway: CompanyUserGateway
    notification_reader: NotificationReader

    async def __call__(
        self, data: GetMyNotificationsInputData
    ) -> GetMyNotificationsOutputData:
        user = await self.id_provider.get_user()

        company_user = await self.company_user_gateway.by_company(
            CompanyId(data.company_id), user.user_id
        )
        if not company_user:
            raise CompanyUserNotFoundError()

        notifications = await self.notification_reader.many(
            NotificationFilters(
                company_user_id=company_user.company_user_id,
                status=data.status,
            ),
            data.pagination,
        )

        return GetMyNotificationsOutputData(notifications)

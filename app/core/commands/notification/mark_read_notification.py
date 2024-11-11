from dataclasses import dataclass

from app.core.commands.company.errors import CompanyUserNotFoundError
from app.core.commands.notification.errors import NotificationNotFoundError
from app.core.commands.user.errors import AccessDeniedError
from app.core.common.commiter import Commiter
from app.core.entities.notification import NotificationId, NotificationStatus
from app.core.interfaces.company_gateways import CompanyUserGateway
from app.core.interfaces.id_provider import IdProvider
from app.core.interfaces.notification_gateways import NotificationGateway


@dataclass(frozen=True)
class MarkReadNotificationInputData:
    notification_id: int


@dataclass
class MarkReadNotification:
    id_provider: IdProvider
    company_user_gateway: CompanyUserGateway
    notification_gateway: NotificationGateway
    commiter: Commiter

    async def __call__(self, data: MarkReadNotificationInputData):
        user = await self.id_provider.get_user()

        company_user = await self.company_user_gateway.by_identity(
            user.user_id
        )
        if not company_user:
            raise CompanyUserNotFoundError()

        notification = await self.notification_gateway.by_id(
            NotificationId(data.notification_id)
        )
        if not notification:
            raise NotificationNotFoundError(data.notification_id)

        if notification.send_to != company_user.company_user_id:
            raise AccessDeniedError()

        notification.status = NotificationStatus.READ

        await self.commiter.commit()

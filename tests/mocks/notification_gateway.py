from app.core.entities.company import CompanyUserId
from app.core.entities.notification import (
    Notification,
    NotificationId,
    NotificationStatus,
)
from app.core.interfaces.notification_gateways import NotificationGateway


class FakeNotificationMapper(NotificationGateway):
    def __init__(self):
        self.notifications = []
        self.notification = Notification(
            notification_id=NotificationId(1),
            send_to=CompanyUserId(1),
            status=NotificationStatus.NEW,
            text="text",
        )

        self.saved = False

    async def add_many(self, notifications: list[Notification]) -> None:
        self.notifications.append(notifications)

        self.saved = True

    async def by_id(
        self, notification_id: NotificationId
    ) -> Notification | None:
        if self.notification.notification_id == notification_id:
            return self.notification
        return None

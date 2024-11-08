from app.core.entities.notification import Notification
from app.core.interfaces.notification_gateways import NotificationGateway


class FakeNotificationMapper(NotificationGateway):
    def __init__(self):
        self.notifications = []

        self.saved = False

    async def add_many(self, notifications: list[Notification]) -> None:
        self.notifications.append(notifications)

        self.saved = True

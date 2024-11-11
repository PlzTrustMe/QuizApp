from dataclasses import dataclass

from app.core.common.base_error import ApplicationError


@dataclass(eq=False)
class NotificationNotFoundError(ApplicationError):
    notification_id: int

    @property
    def message(self) -> str:
        return f"Notification with id {self.notification_id} not found"

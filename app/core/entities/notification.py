from dataclasses import dataclass
from enum import Enum
from typing import NewType

from app.core.entities.company import CompanyUserId

NotificationId = NewType("NotificationId", int)


class NotificationStatus(str, Enum):
    NEW = "new"
    READ = "read"


@dataclass
class Notification:
    notification_id: NotificationId | None
    send_to: CompanyUserId
    text: str
    status: NotificationStatus = NotificationStatus.NEW

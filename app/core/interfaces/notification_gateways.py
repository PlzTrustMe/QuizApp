from abc import abstractmethod
from asyncio import Protocol
from dataclasses import dataclass

from app.core.common.pagination import Pagination
from app.core.entities.notification import (
    Notification,
    NotificationId,
    NotificationStatus,
)


class NotificationGateway(Protocol):
    @abstractmethod
    async def add_many(self, notifications: list[Notification]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def by_id(
        self, notification_id: NotificationId
    ) -> Notification | None:
        raise NotImplementedError


@dataclass
class NotificationFilters:
    company_user_id: int | None = None
    status: NotificationStatus | None = None


@dataclass(frozen=True)
class NotificationDetail:
    notification_id: int
    text: str
    status: NotificationStatus


class NotificationReader(Protocol):
    @abstractmethod
    async def many(
        self, filters: NotificationFilters, pagination: Pagination
    ) -> list[NotificationDetail]:
        raise NotImplementedError

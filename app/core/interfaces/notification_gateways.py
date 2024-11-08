from asyncio import Protocol

from app.core.entities.notification import Notification


class NotificationGateway(Protocol):
    async def add_many(self, notifications: list[Notification]) -> None:
        raise NotImplementedError

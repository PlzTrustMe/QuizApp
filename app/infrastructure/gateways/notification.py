from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.user.errors import UnexpectedError
from app.core.entities.notification import Notification
from app.core.interfaces.notification_gateways import NotificationGateway


class NotificationMapper(NotificationGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_many(self, notifications: list[Notification]) -> None:
        self.session.add_all(notifications)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error

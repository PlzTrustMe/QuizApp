from sqlalchemy import RowMapping, Select, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.user.errors import UnexpectedError
from app.core.common.pagination import Pagination, SortOrder
from app.core.entities.notification import Notification, NotificationId
from app.core.interfaces.notification_gateways import (
    NotificationDetail,
    NotificationFilters,
    NotificationGateway,
    NotificationReader,
)
from app.infrastructure.persistence.models.notification import (
    notifications_table,
)


class NotificationMapper(NotificationGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_many(self, notifications: list[Notification]) -> None:
        self.session.add_all(notifications)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error

    async def by_id(self, notification_id: NotificationId) -> Notification:
        query = select(Notification).where(
            notifications_table.c.notification_id == notification_id
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()


class SQLAlchemyNotificationReader(NotificationReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _make_filters(
        self, query: Select, filters: NotificationFilters
    ) -> Select:
        if filters.company_user_id:
            query = query.where(
                notifications_table.c.send_to == filters.company_user_id
            )

        if filters.status:
            query = query.where(notifications_table.c.status == filters.status)

        return query

    def _load_model(self, row: RowMapping) -> NotificationDetail:
        return NotificationDetail(
            notification_id=row.notification_id,
            text=row.text,
            status=row.status,
        )

    async def many(
        self, filters: NotificationFilters, pagination: Pagination
    ) -> list[NotificationDetail]:
        query = select(
            notifications_table.c.notification_id,
            notifications_table.c.text,
            notifications_table.c.status,
        )

        query = self._make_filters(query, filters)

        if pagination.order is SortOrder.ASC:
            query = query.order_by(notifications_table.c.created_at.asc())
        else:
            query = query.order_by(notifications_table.c.created_at.desc())

        if pagination.offset is not None:
            query = query.offset(pagination.offset)
        if pagination.limit is not None:
            query = query.limit(pagination.limit)

        result = await self.session.execute(query)

        return [self._load_model(row) for row in result.mappings()]

import pytest

from app.core.commands.company.errors import CompanyUserNotFoundError
from app.core.commands.notification.errors import NotificationNotFoundError
from app.core.commands.notification.mark_read_notification import (
    MarkReadNotification,
    MarkReadNotificationInputData,
)
from app.core.entities.notification import NotificationStatus
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import (
    FakeCompanyUserMapper,
)
from tests.mocks.id_provider import FakeIdProvider
from tests.mocks.notification_gateway import FakeNotificationMapper


@pytest.mark.parametrize(
    ["notification_id", "user_id", "exc_class"],
    [
        (1, 2, None),
        (2, 2, NotificationNotFoundError),
        (1, 1, CompanyUserNotFoundError),
    ],
)
async def test_mark_read_notification(
    id_provider: FakeIdProvider,
    company_user_gateway: FakeCompanyUserMapper,
    notification_gateway: FakeNotificationMapper,
    commiter: FakeCommiter,
    notification_id: int,
    user_id: int,
    exc_class,
) -> None:
    id_provider.user.user_id = user_id

    command = MarkReadNotification(
        id_provider, company_user_gateway, notification_gateway, commiter
    )
    input_data = MarkReadNotificationInputData(notification_id)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert (
            notification_gateway.notification.status == NotificationStatus.NEW
        )
        assert not commiter.commited
    else:
        await coro

        assert (
            notification_gateway.notification.status == NotificationStatus.READ
        )
        assert commiter.commited

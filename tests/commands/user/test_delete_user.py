import pytest

from app.core.commands.user.delete_user import DeleteUser, DeleteUserInputData
from app.core.commands.user.errors import UserNotFoundError
from app.core.common.access_service import AccessService
from tests.mocks.commiter import FakeCommiter
from tests.mocks.user_gateways import FakeUserMapper


@pytest.mark.parametrize(
    ["user_id", "exc_class"], [(1, None), (2, UserNotFoundError)]
)
async def test_delete_user(
    user_gateway: FakeUserMapper,
    commiter: FakeCommiter,
    access_service: AccessService,
    user_id: int,
    exc_class,
) -> None:
    command = DeleteUser(user_gateway, commiter, access_service)
    input_data = DeleteUserInputData(user_id)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not commiter.commited
        assert not user_gateway.deleted
    else:
        await coro

        assert commiter.commited
        assert user_gateway.deleted

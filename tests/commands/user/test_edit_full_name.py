import pytest

from app.core.commands.user.edit_full_name import (
    EditFullName,
    EditFullNameInputData,
    EditFullNameOutputData,
)
from app.core.commands.user.errors import UserNotFoundError
from app.core.common.access_service import AccessService
from app.core.entities.value_objects import FullName
from tests.mocks.commiter import FakeCommiter
from tests.mocks.user_gateways import FakeUserMapper


@pytest.mark.parametrize(
    ["user_id", "exc_class"], [(1, None), (2, UserNotFoundError)]
)
async def test_full_name(
    user_gateway: FakeUserMapper,
    access_service: AccessService,
    commiter: FakeCommiter,
    user_id: int,
    exc_class,
) -> None:
    full_name = FullName("NewTest", "NewTestovich")

    command = EditFullName(user_gateway, access_service, commiter)
    input_data = EditFullNameInputData(user_id, "NewTest", "NewTestovich")

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not commiter.commited
    else:
        output_data = await coro

        assert output_data
        assert isinstance(output_data, EditFullNameOutputData)

        assert commiter.commited

        assert user_gateway.user.full_name == full_name
        assert user_gateway.user.user_id == output_data.user_id

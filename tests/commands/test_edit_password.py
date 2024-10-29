import pytest

from app.core.commands.edit_password import EditPassword, EditPasswordInputData
from app.core.commands.errors import PasswordMismatchError, UserNotFoundError
from app.core.common.access_service import AccessService
from app.core.entities.value_objects import UserRawPassword
from app.core.interfaces.password_hasher import PasswordHasher
from tests.mocks.commiter import FakeCommiter
from tests.mocks.user_gateways import FakeUserMapper


@pytest.mark.parametrize(
    ["user_id", "pwd_startswith", "exc_class"],
    [
        (1, "", None),
        (2, "", UserNotFoundError),
        (1, "abc", PasswordMismatchError),
    ],
)
async def test_edit_password(
    user_gateway: FakeUserMapper,
    password_hasher: PasswordHasher,
    access_service: AccessService,
    commiter: FakeCommiter,
    user_pwd: UserRawPassword,
    user_id: int,
    pwd_startswith: str,
    exc_class,
):
    command = EditPassword(
        user_gateway, password_hasher, access_service, commiter
    )
    input_data = EditPasswordInputData(
        user_id=user_id,
        old_password=pwd_startswith + user_pwd.to_raw(),
        new_password=user_pwd.to_raw(),
    )

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not commiter.commited
    else:
        await coro

        assert commiter.commited

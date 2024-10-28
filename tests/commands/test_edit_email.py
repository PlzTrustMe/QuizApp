import pytest

from app.core.commands.edit_email import EditEmail, EditEmailInputData
from app.core.commands.errors import AccessDeniedError
from app.core.common.access_service import AccessService
from tests.mocks.commiter import FakeCommiter
from tests.mocks.user_gateways import FakeUserMapper


async def test_access_denied_edit_email(
    user_gateway: FakeUserMapper,
    access_service: AccessService,
    commiter: FakeCommiter,
):
    new_email = "new_email@gmail.com"

    command = EditEmail(user_gateway, access_service, commiter)
    input_data = EditEmailInputData(1, new_email)

    with pytest.raises(AccessDeniedError):
        await command(input_data)

    assert user_gateway.user.email != new_email
    assert not commiter.commited

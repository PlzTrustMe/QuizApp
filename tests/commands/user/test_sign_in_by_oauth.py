from app.core.commands.user.sign_in_by_oauth import (
    SignInByOauth,
    SignInByOauthInputData,
)
from app.core.entities.value_objects import UserEmail
from tests.mocks.commiter import FakeCommiter
from tests.mocks.user_gateways import FakeUserMapper


async def test_sign_in_by_oath(
    user_gateway: FakeUserMapper,
    commiter: FakeCommiter,
    user_email: UserEmail,
) -> None:
    command = SignInByOauth(user_gateway, commiter)
    input_data = SignInByOauthInputData("new_user@gmail.com")

    await command(input_data)

    assert user_gateway.saved
    assert commiter.commited

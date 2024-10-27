import pytest

from app.core.commands.errors import PasswordMismatchError
from app.core.commands.sign_in import AccessTokenData, SignIn, SignInInputData
from app.core.entities.value_objects import UserEmail, UserRawPassword
from app.core.interfaces.password_hasher import PasswordHasher
from tests.mocks.user_gateways import FakeUserMapper


@pytest.mark.parametrize(
    ["pwd_startswith", "exc_class"],
    [("", None), ("blabla", PasswordMismatchError)],
)
async def test_sign_in(
    user_gateway: FakeUserMapper,
    password_hasher: PasswordHasher,
    user_email: UserEmail,
    user_pwd: UserRawPassword,
    pwd_startswith: str,
    exc_class,
) -> None:
    interactor = SignIn(user_gateway, password_hasher)
    input_data = SignInInputData(
        email=user_email.to_row(), password=user_pwd.to_raw() + pwd_startswith
    )

    coro = interactor(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro
    else:
        output_data = await coro

        assert output_data is not None
        assert isinstance(output_data, AccessTokenData)

        assert output_data.email == user_gateway.user.email.to_row()

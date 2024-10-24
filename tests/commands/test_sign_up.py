import pytest

from app.core.commands.errors import UserEmailAlreadyExistError
from app.core.commands.sign_up import SignUp, SignUpInputData, SignUpOutputData
from app.core.entities.value_objects import UserRawPassword
from app.core.interfaces.password_hasher import PasswordHasher
from tests.mocks.commiter import FakeCommiter
from tests.mocks.user_gateways import FakeUserMapper


@pytest.mark.parametrize(
    ["email", "exc_class"],
    [
        ("test1@gmail.com", None),
        ("test@gmail.com", UserEmailAlreadyExistError),
    ],
)
async def test_sign_up(
    user_gateway: FakeUserMapper,
    password_hasher: PasswordHasher,
    commiter: FakeCommiter,
    user_pwd: UserRawPassword,
    email: str,
    exc_class,
) -> None:
    command = SignUp(
        user_gateway=user_gateway,
        commiter=commiter,
        password_hasher=password_hasher,
    )
    input_data = SignUpInputData(
        email=email,
        password=user_pwd.password,
        first_name="Test",
        last_name="Testovich",
    )

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not commiter.commited
    else:
        output_data = await coro

        assert output_data
        assert isinstance(output_data, SignUpOutputData)

        assert commiter.commited
        assert user_gateway.saved

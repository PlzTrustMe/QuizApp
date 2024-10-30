import pytest

from app.core.commands.user.errors import UserNotFoundError
from app.core.interfaces.user_gateways import UserDetail
from app.core.queries.user.get_user import GetUserById, GetUserByIdInputData
from tests.mocks.user_gateways import FakeUserReader


@pytest.mark.parametrize(
    ["user_id", "exc_class"], [(1, None), (2, UserNotFoundError)]
)
async def test_get_user(
    user_reader: FakeUserReader, user_id: int, exc_class
) -> None:
    query = GetUserById(user_reader)
    input_data = GetUserByIdInputData(user_id)

    coro = query(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro
    else:
        output_data = await coro

        assert output_data
        assert isinstance(output_data, UserDetail)

        assert output_data.user_id == user_id

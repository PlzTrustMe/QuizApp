from app.core.common.pagination import Pagination
from app.core.interfaces.user_gateways import UserFilters
from app.core.queries.user.get_users import (
    GetUsers,
    GetUsersInputData,
    GetUsersOutputData,
)
from tests.mocks.user_gateways import FakeUserReader


async def test_get_users(user_reader: FakeUserReader) -> None:
    query = GetUsers(user_reader)
    input_data = GetUsersInputData(UserFilters(), Pagination())

    output_data = await query(input_data)

    assert output_data
    assert isinstance(output_data, GetUsersOutputData)

    assert output_data.total == len(output_data.users)

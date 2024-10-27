from app.core.interfaces.user_gateways import UserDetail
from app.core.queries.get_me import GetMe
from tests.mocks.id_provider import FakeIdProvider


async def test_get_me(id_provider: FakeIdProvider) -> None:
    query = GetMe(id_provider=id_provider)

    output_data = await query()

    assert output_data
    assert isinstance(output_data, UserDetail)
    assert output_data.user_id == id_provider.user.user_id
    assert id_provider.requested

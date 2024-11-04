import pytest

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.commands.invitation.send_request_from_user import (
    SendRequestFromUser,
    SendRequestFromUserInputData,
)
from app.core.common.access_service import AccessService
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import FakeCompanyMapper
from tests.mocks.id_provider import FakeIdProvider
from tests.mocks.invitation_gateways import FakeUserRequestMapper


@pytest.mark.parametrize(
    ["company_id", "exc_class"], [(2, CompanyNotFoundError)]
)
async def test_send_request_from_user(
    id_provider: FakeIdProvider,
    access_service: AccessService,
    company_gateway: FakeCompanyMapper,
    user_request_gateway: FakeUserRequestMapper,
    commiter: FakeCommiter,
    company_id: int,
    exc_class,
) -> None:
    command = SendRequestFromUser(
        id_provider,
        access_service,
        company_gateway,
        user_request_gateway,
        commiter,
    )
    input_data = SendRequestFromUserInputData(company_id)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not user_request_gateway.saved
        assert not commiter.commited
    else:
        await coro

        assert user_request_gateway.user_request.company_id == company_id
        assert user_request_gateway.saved
        assert commiter.commited

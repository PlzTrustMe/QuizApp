import pytest

from app.core.commands.invitation.errors import (
    UserRequestNotFoundError,
)
from app.core.commands.invitation.reject_user_request import (
    RejectUserRequest,
    RejectUserRequestInputData,
)
from app.core.common.access_service import AccessService
from app.core.entities.invitation import RequestStatus
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import FakeCompanyMapper
from tests.mocks.invitation_gateways import (
    FakeUserRequestMapper,
)


@pytest.mark.parametrize(
    ["user_request_id", "exc_class"],
    [(1, None), (2, UserRequestNotFoundError)],
)
async def test_reject_invitation(
    access_service: AccessService,
    user_request_gateway: FakeUserRequestMapper,
    company_gateway: FakeCompanyMapper,
    commiter: FakeCommiter,
    user_request_id: int,
    exc_class,
) -> None:
    command = RejectUserRequest(
        access_service, user_request_gateway, company_gateway, commiter
    )
    input_data = RejectUserRequestInputData(user_request_id)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not commiter.commited
        assert user_request_gateway.user_request.status == RequestStatus.NEW
    else:
        await coro

        assert commiter.commited
        assert (
            user_request_gateway.user_request.status == RequestStatus.REJECTED
        )

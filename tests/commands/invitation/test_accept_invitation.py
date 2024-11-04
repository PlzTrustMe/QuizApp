import pytest

from app.core.commands.invitation.accept_invitation import (
    AcceptInvitation,
    AcceptInvitationInputData,
)
from app.core.commands.invitation.errors import InvitationNotFoundError
from app.core.common.access_service import AccessService
from app.core.entities.invitation import RequestStatus
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import (
    FakeCompanyMapper,
    FakeCompanyUserMapper,
)
from tests.mocks.invitation_gateways import FakeInvitationMapper


@pytest.mark.parametrize(
    ["invitation_id", "exc_class"], [(1, None), (2, InvitationNotFoundError)]
)
async def test_accept_invitation(
    access_service: AccessService,
    invitation_gateway: FakeInvitationMapper,
    company_gateway: FakeCompanyMapper,
    company_user_gateway: FakeCompanyUserMapper,
    commiter: FakeCommiter,
    invitation_id: int,
    exc_class,
) -> None:
    command = AcceptInvitation(
        access_service,
        invitation_gateway,
        company_gateway,
        company_user_gateway,
        commiter,
    )
    input_data = AcceptInvitationInputData(invitation_id)
    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not commiter.commited
        assert invitation_gateway.invitation.status == RequestStatus.NEW
    else:
        await coro

        assert commiter.commited
        assert invitation_gateway.invitation.status == RequestStatus.ACCEPTED

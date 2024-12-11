import pytest

from app.core.commands.company.errors import CompanyNotFoundError
from app.core.commands.invitation.errors import InvitationAlreadyExistError
from app.core.commands.invitation.send_invitation_to_user import (
    SendInvitationToUser,
    SendInvitationToUserInputData,
)
from app.core.commands.user.errors import UserNotFoundError
from app.core.common.access_service import AccessService
from app.core.interfaces.user_gateways import UserGateway
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import FakeCompanyMapper
from tests.mocks.invitation_gateways import FakeInvitationMapper


@pytest.mark.parametrize(
    ["company_id", "user_id", "exc_class"],
    [
        (2, 1, CompanyNotFoundError),
        (1, 2, UserNotFoundError),
        (1, 1, InvitationAlreadyExistError),
    ],
)
async def test_send_invitation_to_user(
    access_service: AccessService,
    invitation_gateway: FakeInvitationMapper,
    company_gateway: FakeCompanyMapper,
    user_gateway: UserGateway,
    commiter: FakeCommiter,
    company_id: int,
    user_id: int,
    exc_class,
) -> None:
    command = SendInvitationToUser(
        access_service,
        invitation_gateway,
        company_gateway,
        user_gateway,
        commiter,
    )
    input_data = SendInvitationToUserInputData(company_id, user_id)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not invitation_gateway.saved
        assert not commiter.commited
    else:
        await coro

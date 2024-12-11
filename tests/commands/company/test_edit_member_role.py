import pytest

from app.core.commands.company.edit_member_role import (
    EditMemberRole,
    EditMemberRoleInputData,
)
from app.core.commands.company.errors import (
    CompanyNotFoundError,
    CompanyUserNotFoundError,
)
from app.core.commands.user.errors import AccessDeniedError
from app.core.common.access_service import AccessService
from app.core.entities.company import CompanyRole
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import (
    FakeCompanyMapper,
    FakeCompanyUserMapper,
)
from tests.mocks.id_provider import FakeIdProvider


@pytest.mark.parametrize(
    ["user_id", "actor_id", "company_id", "role", "exc_class"],
    [
        (2, 1, 1, CompanyRole.ADMIN, None),
        (1, 1, 1, CompanyRole.ADMIN, CompanyUserNotFoundError),
        (2, 2, 1, CompanyRole.ADMIN, AccessDeniedError),
        (2, 1, 2, CompanyRole.ADMIN, CompanyNotFoundError),
    ],
)
async def test_edit_member_role(
    access_service: AccessService,
    company_gateway: FakeCompanyMapper,
    company_user_gateway: FakeCompanyUserMapper,
    commiter: FakeCommiter,
    id_provider: FakeIdProvider,
    user_id: int,
    actor_id: int,
    company_id: int,
    role: CompanyRole,
    exc_class,
) -> None:
    id_provider.user.user_id = actor_id
    old_role = company_user_gateway.company_user.role

    command = EditMemberRole(
        access_service, company_user_gateway, company_gateway, commiter
    )
    input_data = EditMemberRoleInputData(user_id, company_id, role)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not commiter.commited
        assert old_role == company_user_gateway.company_user.role
    else:
        await coro

        assert commiter.commited
        assert company_user_gateway.company_user.role == role

import pytest

from app.core.commands.company.errors import (
    CompanyNotFoundError,
    CompanyUserNotFoundError,
)
from app.core.commands.company.leave_from_company import (
    LeaveFromCompany,
    LeaveFromCompanyInputData,
)
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import (
    FakeCompanyMapper,
    FakeCompanyUserMapper,
)
from tests.mocks.id_provider import FakeIdProvider


@pytest.mark.parametrize(
    ["company_id", "user_id", "exc_class"],
    [
        (1, 2, None),
        (1, 1, CompanyUserNotFoundError),
        (2, 2, CompanyNotFoundError),
    ],
)
async def test_leave_from_company(
    id_provider: FakeIdProvider,
    company_gateway: FakeCompanyMapper,
    company_user_gateway: FakeCompanyUserMapper,
    commiter: FakeCommiter,
    company_id: int,
    user_id: int,
    exc_class,
) -> None:
    id_provider.user.user_id = user_id

    command = LeaveFromCompany(
        id_provider, company_gateway, company_user_gateway, commiter
    )
    input_data = LeaveFromCompanyInputData(company_id)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not company_user_gateway.deleted
        assert not commiter.commited
    else:
        await coro

        assert company_user_gateway.deleted
        assert commiter.commited

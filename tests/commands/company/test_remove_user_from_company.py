import pytest

from app.core.commands.company.errors import (
    CompanyNotFoundError,
    CompanyUserNotFoundError,
)
from app.core.commands.company.remove_user_from_company import (
    RemoveUserFromCompany,
    RemoveUserFromCompanyInputData,
)
from app.core.common.access_service import AccessService
from tests.mocks.company_gateways import (
    FakeCompanyMapper,
    FakeCompanyUserMapper,
)


@pytest.mark.parametrize(
    ["company_id", "user_id", "exc_class"],
    [
        (1, 2, None),
        (1, 1, CompanyUserNotFoundError),
        (2, 2, CompanyNotFoundError),
    ],
)
async def test_remove_user_from_company(
    company_gateway: FakeCompanyMapper,
    company_user_gateway: FakeCompanyUserMapper,
    access_service: AccessService,
    company_id: int,
    user_id: int,
    exc_class,
) -> None:
    command = RemoveUserFromCompany(
        company_gateway, company_user_gateway, access_service
    )
    input_data = RemoveUserFromCompanyInputData(company_id, user_id)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not company_user_gateway.deleted
    else:
        await coro

        assert company_user_gateway.deleted

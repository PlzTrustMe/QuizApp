import pytest

from app.core.commands.company.edit_company_name import (
    EditCompanyName,
    EditCompanyNameInputData,
)
from app.core.commands.company.errors import CompanyNotFoundError
from app.core.common.access_service import AccessService
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import FakeCompanyMapper


@pytest.mark.parametrize(
    ["company_id", "new_name", "exc_class"],
    [(1, "NewName", None), (2, "NewName", CompanyNotFoundError)],
)
async def test_edit_company_name(
    company_gateway: FakeCompanyMapper,
    access_service: AccessService,
    commiter: FakeCommiter,
    company_id: int,
    new_name: str,
    exc_class,
):
    command = EditCompanyName(company_gateway, access_service, commiter)
    input_data = EditCompanyNameInputData(company_id, new_name)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not commiter.commited
    else:
        await coro

        assert company_gateway.company.name.to_raw() == new_name
        assert commiter.commited

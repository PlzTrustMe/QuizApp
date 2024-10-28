import pytest

from app.core.commands.company.delete_company import (
    DeleteCompany,
    DeleteCompanyInputData,
)
from app.core.commands.company.errors import CompanyNotFoundError
from app.core.common.access_service import AccessService
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import FakeCompanyMapper


@pytest.mark.parametrize(
    ["company_id", "exc_class"],
    [(1, None), (2, CompanyNotFoundError)],
)
async def test_edit_company_description(
    company_gateway: FakeCompanyMapper,
    access_service: AccessService,
    commiter: FakeCommiter,
    company_id: int,
    exc_class,
):
    command = DeleteCompany(company_gateway, access_service, commiter)
    input_data = DeleteCompanyInputData(company_id)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not commiter.commited
        assert not company_gateway.deleted
    else:
        await coro

        assert commiter.commited
        assert company_gateway.deleted

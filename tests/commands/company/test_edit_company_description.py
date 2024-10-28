import pytest

from app.core.commands.company.edit_company_description import (
    EditCompanyDescription,
    EditCompanyDescriptionInputData,
)
from app.core.commands.company.errors import CompanyNotFoundError
from app.core.common.access_service import AccessService
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import FakeCompanyMapper


@pytest.mark.parametrize(
    ["company_id", "new_desc", "exc_class"],
    [(1, "NewDesc", None), (2, "", CompanyNotFoundError)],
)
async def test_edit_company_name(
    company_gateway: FakeCompanyMapper,
    access_service: AccessService,
    commiter: FakeCommiter,
    company_id: int,
    new_desc: str,
    exc_class,
):
    command = EditCompanyDescription(company_gateway, access_service, commiter)
    input_data = EditCompanyDescriptionInputData(company_id, new_desc)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not commiter.commited
    else:
        await coro

        assert company_gateway.company.description.to_raw() == new_desc
        assert commiter.commited

import pytest

from app.core.commands.company.edit_company_visibility import (
    EditCompanyVisibility,
    EditCompanyVisibilityInputData,
)
from app.core.commands.company.errors import CompanyNotFoundError
from app.core.common.access_service import AccessService
from app.core.entities.company import Visibility
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import FakeCompanyMapper


@pytest.mark.parametrize(
    ["company_id", "visibility", "exc_class"],
    [(1, Visibility.HIDDEN, None), (2, "NewName", CompanyNotFoundError)],
)
async def test_edit_company_visibility(
    company_gateway: FakeCompanyMapper,
    access_service: AccessService,
    commiter: FakeCommiter,
    company_id: int,
    visibility: Visibility,
    exc_class,
):
    command = EditCompanyVisibility(company_gateway, access_service, commiter)
    input_data = EditCompanyVisibilityInputData(company_id, visibility)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not commiter.commited
    else:
        await coro

        assert company_gateway.company.visibility == visibility
        assert commiter.commited

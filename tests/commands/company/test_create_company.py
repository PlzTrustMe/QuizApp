import pytest

from app.core.commands.company.create_company import (
    CreateCompany,
    CreateCompanyInputData,
)
from app.core.commands.company.errors import CompanyWithNameAlreadyExistError
from tests.mocks.commiter import FakeCommiter
from tests.mocks.company_gateways import (
    FakeCompanyMapper,
    FakeCompanyUserMapper,
)
from tests.mocks.id_provider import FakeIdProvider


@pytest.mark.parametrize(
    ["name", "desc", "exc_class"],
    [
        ("NewTest", "", None),
        ("NewTestCompany", "", CompanyWithNameAlreadyExistError),
    ],
)
async def test_create_company(
    id_provider: FakeIdProvider,
    company_gateway: FakeCompanyMapper,
    company_user_gateway: FakeCompanyUserMapper,
    commiter: FakeCommiter,
    name: str,
    desc: str,
    exc_class,
) -> None:
    command = CreateCompany(
        id_provider, company_gateway, company_user_gateway, commiter
    )
    input_data = CreateCompanyInputData(name, desc)

    coro = command(input_data)

    if exc_class:
        with pytest.raises(exc_class):
            await coro

        assert not commiter.commited
    else:
        await coro

        assert company_gateway.company.name.to_raw() == name
        assert company_gateway.company.description.to_raw() == desc
        assert commiter.commited

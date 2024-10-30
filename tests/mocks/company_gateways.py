from app.core.entities.company import (
    Company,
    CompanyId,
    CompanyRole,
    CompanyUser,
    CompanyUserId,
    Visibility,
)
from app.core.entities.user import UserId
from app.core.entities.value_objects import CompanyDescription, CompanyName
from app.core.interfaces.company_gateways import (
    CompanyGateway,
    CompanyUserGateway,
)


class FakeCompanyMapper(CompanyGateway):
    def __init__(self):
        self.company = Company(
            company_id=CompanyId(1),
            owner_id=UserId(1),
            name=CompanyName("NewTestCompany"),
            description=CompanyDescription(""),
            visibility=Visibility.VISIBLE,
        )
        self.saved = False
        self.deleted = False

    async def add(self, company: Company) -> None:
        self.company.name = company.name
        self.company.description = company.description
        self.company.visibility = company.visibility

        self.saved = True

    async def is_exist(self, name: CompanyName) -> bool:
        return self.company.name == name

    async def by_id(self, company_id: CompanyId) -> Company | None:
        if self.company.company_id == company_id:
            return self.company
        return None

    async def delete(self, company_id: CompanyId) -> None:
        if self.company.company_id == company_id:
            self.deleted = True


class FakeCompanyUserMapper(CompanyUserGateway):
    def __init__(self):
        self.company_user = CompanyUser(
            company_user_id=CompanyUserId(1),
            company_id=CompanyId(1),
            user_id=UserId(2),
            role=CompanyRole.OWNER,
        )

        self.saved = False

    async def add(self, company_user: CompanyUser) -> None:
        self.company_user.role = company_user.role
        self.saved = True

    async def is_exist(self, company_id: CompanyId, user_id: UserId) -> bool:
        return (
            self.company_user.user_id == user_id
            and self.company_user.company_id == company_id
        )

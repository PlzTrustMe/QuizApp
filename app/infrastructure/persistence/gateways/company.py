from sqlalchemy import exists, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.user.errors import UnexpectedError
from app.core.entities.company import Company, CompanyUser
from app.core.entities.value_objects import CompanyName
from app.core.interfaces.company_gateways import (
    CompanyGateway,
    CompanyUserGateway,
)
from app.infrastructure.persistence.models.company import companies_table


class CompanyMapper(CompanyGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, company: Company) -> None:
        self.session.add(company)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error

    async def is_exist(self, name: CompanyName) -> bool:
        query = select(
            exists().where(companies_table.c.company_name == name.value)
        )

        result = await self.session.execute(query)

        return result.scalar()


class CompanyUserMapper(CompanyUserGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, company_user: CompanyUser) -> None:
        self.session.add(CompanyUser)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error

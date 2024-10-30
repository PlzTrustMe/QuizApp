from abc import abstractmethod
from asyncio import Protocol
from dataclasses import dataclass

from app.core.common.pagination import Pagination
from app.core.entities.company import (
    Company,
    CompanyId,
    CompanyUser,
    Visibility,
)
from app.core.entities.user import UserId
from app.core.entities.value_objects import CompanyName


class CompanyGateway(Protocol):
    @abstractmethod
    async def add(self, company: Company) -> None:
        raise NotImplementedError

    @abstractmethod
    async def is_exist(self, name: CompanyName) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def by_id(self, company_id: CompanyId) -> Company | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, company_id: CompanyId) -> None:
        raise NotImplementedError


class CompanyUserGateway(Protocol):
    @abstractmethod
    async def add(self, company_user: CompanyUser) -> None:
        raise NotImplementedError

    @abstractmethod
    async def is_exist(self, company_id: CompanyId, user_id: UserId) -> bool:
        raise NotImplementedError


@dataclass
class CompanyDetail:
    company_id: int
    name: str
    description: str
    visibility: Visibility


@dataclass
class CompanyFilters:
    visibility: Visibility | None = None


class CompanyReader(Protocol):
    @abstractmethod
    async def by_id(self, company_id: CompanyId) -> CompanyDetail:
        raise NotImplementedError

    @abstractmethod
    async def many(
        self, filters: CompanyFilters, pagination: Pagination
    ) -> list[CompanyDetail]:
        raise NotImplementedError

    @abstractmethod
    async def total(self, filters: CompanyFilters) -> int:
        raise NotImplementedError

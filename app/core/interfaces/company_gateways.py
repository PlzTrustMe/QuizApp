from abc import abstractmethod
from asyncio import Protocol

from app.core.entities.company import Company, CompanyUser
from app.core.entities.value_objects import CompanyName


class CompanyGateway(Protocol):
    @abstractmethod
    async def add(self, company: Company) -> None:
        raise NotImplementedError

    @abstractmethod
    async def is_exist(self, name: CompanyName) -> bool:
        raise NotImplementedError


class CompanyUserGateway(Protocol):
    @abstractmethod
    async def add(self, company_user: CompanyUser) -> None:
        raise NotImplementedError

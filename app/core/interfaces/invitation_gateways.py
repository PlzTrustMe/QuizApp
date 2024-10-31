from abc import abstractmethod
from asyncio import Protocol
from dataclasses import dataclass

from app.core.common.pagination import Pagination
from app.core.entities.company import CompanyId
from app.core.entities.invitation import (
    Invitation,
    InvitationId,
    RequestStatus,
    UserRequest,
    UserRequestId,
)
from app.core.entities.user import UserId


@dataclass
class Filters:
    user_id: UserId | None = None
    company_id: CompanyId | None = None


@dataclass
class Details:
    company_id: int
    status: RequestStatus


class InvitationGateway(Protocol):
    @abstractmethod
    async def is_exist(self, company_id: CompanyId, user_id: UserId) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def add(self, invitation: Invitation) -> None:
        raise NotImplementedError

    @abstractmethod
    async def by_id(self, invitation_id: InvitationId) -> Invitation | None:
        raise NotImplementedError


@dataclass
class InvitationFilters(Filters):
    pass


@dataclass
class InvitationDetail(Details):
    invitation_id: int


class InvitationReader(Protocol):
    @abstractmethod
    async def many(
        self, filters: InvitationFilters, pagination: Pagination
    ) -> list[InvitationDetail]:
        raise NotImplementedError

    @abstractmethod
    async def total(self, filters: InvitationFilters) -> int:
        raise NotImplementedError


class UserRequestGateway(Protocol):
    @abstractmethod
    async def is_exist(self, company_id: CompanyId, user_id: UserId) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def add(self, user_request: UserRequest) -> None:
        raise NotImplementedError

    @abstractmethod
    async def by_id(
        self, user_request_id: UserRequestId
    ) -> UserRequest | None:
        raise NotImplementedError


@dataclass
class UserRequestFilters(Filters):
    pass


@dataclass
class UserRequestDetail(Details):
    user_request_id: int


class UserRequestReader(Protocol):
    async def many(
        self, filters: UserRequestFilters, pagination: Pagination
    ) -> list[UserRequestDetail]:
        raise NotImplementedError

    async def total(self, filters: UserRequestFilters) -> int:
        raise NotImplementedError

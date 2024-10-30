from abc import abstractmethod
from asyncio import Protocol

from app.core.entities.company import CompanyId
from app.core.entities.invitation import Invitation, UserRequest
from app.core.entities.user import UserId


class InvitationGateway(Protocol):
    @abstractmethod
    async def is_exist(self, company_id: CompanyId, user_id: UserId) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def add(self, invitation: Invitation) -> None:
        raise NotImplementedError


class UserRequestGateway(Protocol):
    @abstractmethod
    async def is_exist(self, company_id: CompanyId, user_id: UserId) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def add(self, user_request: UserRequest) -> None:
        raise NotImplementedError

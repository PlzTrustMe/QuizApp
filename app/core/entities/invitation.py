from dataclasses import dataclass
from enum import Enum, auto
from typing import NewType

from .company import CompanyId
from .user import UserId

InvitationId = NewType("InvitationId", int)
UserRequestId = NewType("UserRequestId", int)


class RequestStatus(str, Enum):
    NEW = auto()
    ACCEPTED = auto()
    REJECTED = auto()


@dataclass
class Invitation:
    invitation_id: InvitationId | None
    company_id: CompanyId
    user_id: UserId
    status: RequestStatus = RequestStatus.NEW


@dataclass
class UserRequest:
    user_request_id: UserRequestId | None
    company_id: CompanyId
    user_id: UserId
    status: RequestStatus = RequestStatus.NEW

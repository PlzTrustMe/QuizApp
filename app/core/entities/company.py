from dataclasses import dataclass
from enum import Enum
from typing import NewType

from app.core.entities.user import UserId
from app.core.entities.value_objects import CompanyDescription, CompanyName

CompanyId = NewType("CompanyId", int)
CompanyUserId = NewType("CompanyUserId", int)


class Visibility(str, Enum):
    HIDDEN = "hidden"
    VISIBLE = "visible"


class CompanyRole(str, Enum):
    OWNER = "Owner"
    ADMIN = "Admin"
    MEMBER = "Member"


@dataclass
class Company:
    company_id: CompanyId | None
    owner_id: UserId
    name: CompanyName
    description: CompanyDescription
    visibility: Visibility


@dataclass
class CompanyUser:
    company_user_id: CompanyUserId | None
    company_id: CompanyId
    user_id: UserId
    role: CompanyRole

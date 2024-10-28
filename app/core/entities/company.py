from dataclasses import dataclass
from enum import Enum, auto
from typing import NewType

from app.core.entities.user import UserId

CompanyId = NewType("CompanyId", int)


class Visibility(Enum):
    HIDDEN = auto()
    VISIBLE = auto()


@dataclass
class Company:
    company_id: CompanyId | None
    owner_id: UserId
    name: str
    description: str
    visibility: Visibility

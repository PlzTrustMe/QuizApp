from dataclasses import dataclass
from enum import Enum, auto
from typing import NewType

from app.core.entities.user import UserId
from app.core.entities.value_objects import CompanyDescription, CompanyName

CompanyId = NewType("CompanyId", int)


class Visibility(Enum):
    HIDDEN = auto()
    VISIBLE = auto()


@dataclass
class Company:
    company_id: CompanyId | None
    owner_id: UserId
    name: CompanyName
    description: CompanyDescription
    visibility: Visibility

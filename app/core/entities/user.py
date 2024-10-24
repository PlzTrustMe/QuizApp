from dataclasses import dataclass
from typing import NewType

from app.core.entities.value_objects import FullName, UserEmail

UserId = NewType("UserId", int)


@dataclass
class User:
    user_id: UserId | None
    full_name: FullName
    email: UserEmail
    hashed_password: str
    is_active: bool = True

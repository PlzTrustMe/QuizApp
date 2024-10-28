from dataclasses import dataclass

from app.core.common.base_error import ApplicationError


@dataclass(eq=False)
class CompanyWithNameAlreadyExistError(ApplicationError):
    name: str

    @property
    def message(self) -> str:
        return f"Company with name {self.name} already exist"

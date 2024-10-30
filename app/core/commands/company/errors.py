from dataclasses import dataclass

from app.core.common.base_error import ApplicationError


@dataclass(eq=False)
class CompanyWithNameAlreadyExistError(ApplicationError):
    name: str

    @property
    def message(self) -> str:
        return f"Company with name {self.name} already exist"


@dataclass(eq=False)
class CompanyNotFoundError(ApplicationError):
    company_id: int

    @property
    def message(self) -> str:
        return f"Company with id {self.company_id} not found"


@dataclass(eq=False)
class CompanyUserNotFoundError(ApplicationError):
    @property
    def message(self) -> str:
        return "Company user not found"

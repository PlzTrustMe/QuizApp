from dataclasses import dataclass

from app.core.common.base_error import ApplicationError


@dataclass(eq=False)
class InvitationAlreadyExistError(ApplicationError):
    company_id: int
    user_id: int

    @property
    def message(self) -> str:
        return (
            f"Invitation to company {self.company_id} already "
            f"sent to user {self.user_id}"
        )


@dataclass(eq=False)
class InvitationNotFoundError(ApplicationError):
    invitation_id: int

    @property
    def message(self) -> str:
        return f"Invitation with id {self.invitation_id} not found"


@dataclass(eq=False)
class UserRequestAlreadyExistError(ApplicationError):
    company_id: int
    user_id: int

    @property
    def message(self) -> str:
        return (
            f"User request to company {self.company_id} already "
            f"sent from user {self.user_id}"
        )


@dataclass
class CompanyUserAlreadyExistError(ApplicationError):
    company_id: int
    user_id: int

    @property
    def message(self) -> str:
        return (
            f"User {self.user_id} already a member of "
            f"company {self.company_id}"
        )

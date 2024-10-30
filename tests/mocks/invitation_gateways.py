from app.core.entities.company import CompanyId
from app.core.entities.invitation import (
    Invitation,
    InvitationId,
    RequestStatus,
    UserRequest,
    UserRequestId,
)
from app.core.entities.user import UserId
from app.core.interfaces.invitation_gateways import (
    InvitationGateway,
    UserRequestGateway,
)


class FakeInvitationMapper(InvitationGateway):
    def __init__(self):
        self.invitation = Invitation(
            invitation_id=InvitationId(1),
            company_id=CompanyId(1),
            user_id=UserId(1),
        )

        self.saved = False

    async def add(self, invitation: Invitation) -> None:
        self.invitation.company_id = invitation.company_id
        self.invitation.user_id = invitation.user_id

        self.saved = True

    async def is_exist(self, company_id: CompanyId, user_id: UserId) -> bool:
        return (
            self.invitation.company_id == company_id
            and self.invitation.user_id == user_id
            and self.invitation.status == RequestStatus.NEW
        )

    async def by_id(self, invitation_id: InvitationId) -> Invitation | None:
        if self.invitation.invitation_id == invitation_id:
            return self.invitation
        return None


class FakeUserRequestMapper(UserRequestGateway):
    def __init__(self):
        self.user_request = UserRequest(
            user_request_id=UserRequestId(1),
            company_id=CompanyId(1),
            user_id=UserId(2),
        )

        self.saved = False

    async def add(self, user_request: UserRequest) -> None:
        self.user_request.company_id = user_request.company_id
        self.user_request.user_id = user_request.user_id

        self.saved = True

    async def is_exist(self, company_id: CompanyId, user_id: UserId) -> bool:
        return (
            self.user_request.company_id == company_id
            and self.user_request.user_id == user_id
            and self.user_request.status == RequestStatus.NEW
        )

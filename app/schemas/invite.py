from pydantic import BaseModel


class SendInvite(BaseModel):
    company_id: int


class SendInviteToUser(SendInvite):
    user_id: int


class SendReqeustToCompany(SendInvite):
    pass

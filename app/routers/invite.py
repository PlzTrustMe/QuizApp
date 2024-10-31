from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from app.core.commands.invitation.accept_invitation import (
    AcceptInvitation,
    AcceptInvitationInputData,
)
from app.core.commands.invitation.accept_user_request import (
    AcceptUserRequest,
    AcceptUserRequestInputData,
)
from app.core.commands.invitation.reject_invitation import (
    RejectInvitation,
    RejectInvitationInputData,
)
from app.core.commands.invitation.reject_user_request import (
    RejectUserRequest,
    RejectUserRequestInputData,
)
from app.core.commands.invitation.send_invitation_to_user import (
    SendInvitationToUser,
    SendInvitationToUserInputData,
)
from app.core.commands.invitation.send_request_from_user import (
    SendRequestFromUser,
    SendRequestFromUserInputData,
)
from app.core.entities.invitation import InvitationId, UserRequestId
from app.routers.responses.base import OkResponse
from app.schemas.invite import SendInviteToUser, SendReqeustToCompany

invite_router = APIRouter(
    prefix="/invite",
    tags=["Invite"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
    route_class=DishkaRoute,
)


@invite_router.post("/to-user", status_code=status.HTTP_201_CREATED)
async def send_invite_to_user(
    body: SendInviteToUser, action: FromDishka[SendInvitationToUser]
) -> OkResponse[InvitationId]:
    response = await action(
        SendInvitationToUserInputData(
            company_id=body.company_id, user_id=body.user_id
        )
    )

    return OkResponse(status=201, result=response)


@invite_router.post("/to-company", status_code=status.HTTP_201_CREATED)
async def send_reqeust_to_company(
    body: SendReqeustToCompany, action: FromDishka[SendRequestFromUser]
) -> OkResponse[UserRequestId]:
    response = await action(
        SendRequestFromUserInputData(company_id=body.company_id)
    )

    return OkResponse(status=201, result=response)


@invite_router.put(
    "/invitation/{invitation_id}/reject", status_code=status.HTTP_200_OK
)
async def reject_invite_to_user(
    invitation_id: int, action: FromDishka[RejectInvitation]
) -> OkResponse:
    await action(RejectInvitationInputData(invitation_id=invitation_id))

    return OkResponse()


@invite_router.put(
    "/user_request/{user_request_id}/reject", status_code=status.HTTP_200_OK
)
async def reject_user_request(
    user_request_id: int, action: FromDishka[RejectUserRequest]
) -> OkResponse:
    await action(RejectUserRequestInputData(request_id=user_request_id))

    return OkResponse()


@invite_router.put(
    "/invitation/{invitation_id}/accept", status_code=status.HTTP_200_OK
)
async def accept_invitation(
    invitation_id: int, action: FromDishka[AcceptInvitation]
) -> OkResponse:
    await action(AcceptInvitationInputData(invitation_id))

    return OkResponse()


@invite_router.put(
    "/user_request/{user_request_id}/accept", status_code=status.HTTP_200_OK
)
async def accept_user_request(
    user_request_id: int, action: FromDishka[AcceptUserRequest]
) -> OkResponse:
    await action(AcceptUserRequestInputData(user_request_id))

    return OkResponse()

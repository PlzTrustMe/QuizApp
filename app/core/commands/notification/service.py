from app.core.entities.company import Company
from app.core.entities.notification import Notification
from app.core.interfaces.company_gateways import (
    CompanyUserFilters,
    CompanyUserGateway,
)
from app.core.interfaces.notification_gateways import NotificationGateway


class NotificationService:
    def __init__(
        self,
        notification_gateway: NotificationGateway,
        company_user_gateway: CompanyUserGateway,
    ) -> None:
        self.notification_gateway = notification_gateway
        self.company_user_gateway = company_user_gateway

    async def send_notification(self, text: str, company: Company):
        company_users = await self.company_user_gateway.many(
            CompanyUserFilters(company.company_id)
        )

        notifications = [
            Notification(
                notification_id=None, text=text, send_to=user.company_user_id
            )
            for user in company_users
        ]

        await self.notification_gateway.add_many(notifications)

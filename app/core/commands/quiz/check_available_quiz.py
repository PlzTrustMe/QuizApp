from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from app.core.common.commiter import Commiter
from app.core.entities.notification import Notification
from app.core.interfaces.company_gateways import CompanyGateway
from app.core.interfaces.notification_gateways import NotificationGateway
from app.core.interfaces.quiz_gateways import (
    QuizParticipationGateway,
)


@dataclass
class CheckAvailableQuiz:
    participation_gateway: QuizParticipationGateway
    notification_gateway: NotificationGateway
    company_gateway: CompanyGateway
    commiter: Commiter

    async def __call__(self) -> None:
        participations = await self.participation_gateway.many()
        now = datetime.now(tz=UTC)

        notifications = [
            Notification(
                notification_id=None,
                text=f"It's time to re-run the quiz {participation.quiz_id}",
                send_to=participation.company_user_id,
            )
            for participation in participations
            if (now - participation.created_at.replace(tzinfo=UTC))
            >= timedelta(hours=24)
        ]

        if len(notifications) > 0:
            await self.notification_gateway.add_many(notifications)
            await self.commiter.commit()

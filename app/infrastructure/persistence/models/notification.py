import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.core.entities.notification import Notification, NotificationStatus

from .base import mapper_registry

notifications_table = sa.Table(
    "notifications",
    mapper_registry.metadata,
    sa.Column(
        "notification_id",
        sa.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    ),
    sa.Column(
        "send_to",
        sa.Integer,
        sa.ForeignKey("company_users.company_user_id", ondelete="CASCADE"),
    ),
    sa.Column("text", sa.String(length=128), nullable=False),
    sa.Column(
        "status", sa.Enum(NotificationStatus), default=NotificationStatus.NEW
    ),
    sa.Column(
        "created_at",
        sa.DateTime,
        default=sa.func.now(),
        server_default=sa.func.now(),
    ),
    sa.Column(
        "updated_at",
        sa.DateTime,
        default=sa.func.now(),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        server_onupdate=sa.func.now(),
    ),
)


def map_notifications_table() -> None:
    mapper_registry.map_imperatively(
        Notification,
        notifications_table,
        properties={
            "company_user": relationship(
                "CompanyUser", back_populates="notification"
            )
        },
    )

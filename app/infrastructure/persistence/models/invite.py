import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.core.entities.invitation import Invitation, RequestStatus, UserRequest

from .base import mapper_registry

invitations_table = sa.Table(
    "invitations",
    mapper_registry.metadata,
    sa.Column(
        "invitation_id",
        sa.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    ),
    sa.Column("status", sa.Enum(RequestStatus), default=RequestStatus.NEW),
    sa.Column(
        "company_id",
        sa.Integer,
        sa.ForeignKey("companies.company_id", ondelete="CASCADE"),
    ),
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("users.user_id", ondelete="CASCADE"),
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

user_requests_table = sa.Table(
    "user_requests",
    mapper_registry.metadata,
    sa.Column(
        "user_request_id",
        sa.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    ),
    sa.Column("status", sa.Enum(RequestStatus), default=RequestStatus.NEW),
    sa.Column(
        "company_id",
        sa.Integer,
        sa.ForeignKey("companies.company_id", ondelete="CASCADE"),
    ),
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("users.user_id", ondelete="CASCADE"),
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


def map_invitations_table() -> None:
    mapper_registry.map_imperatively(
        Invitation,
        invitations_table,
        properties={
            "user": relationship("User", back_populates="invitation"),
            "company": relationship("Company", back_populates="invitation"),
        },
    )


def map_user_requests_table() -> None:
    mapper_registry.map_imperatively(
        UserRequest,
        user_requests_table,
        properties={
            "user": relationship("User", back_populates="user_request"),
            "company": relationship("Company", back_populates="user_request"),
        },
    )

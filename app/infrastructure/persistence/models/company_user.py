import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.core.entities.company import CompanyRole, CompanyUser

from .base import mapper_registry

company_users_table = sa.Table(
    "company_users",
    mapper_registry.metadata,
    sa.Column(
        "company_user_id",
        sa.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    ),
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
    sa.Column("role", sa.Enum(CompanyRole)),
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


def map_company_users_table() -> None:
    mapper_registry.map_imperatively(
        CompanyUser,
        company_users_table,
        properties={
            "user": relationship("User", back_populates="company_user"),
            "company": relationship("Company", back_populates="company_user"),
        },
    )

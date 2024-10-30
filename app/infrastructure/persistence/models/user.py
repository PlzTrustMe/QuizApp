import sqlalchemy as sa
from sqlalchemy.orm import composite, relationship

from app.core.entities.user import User
from app.core.entities.value_objects import FullName, UserEmail
from app.infrastructure.persistence.models.base import mapper_registry

users_table = sa.Table(
    "users",
    mapper_registry.metadata,
    sa.Column(
        "user_id",
        sa.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    ),
    sa.Column("first_name", sa.String(length=15), nullable=True, default=None),
    sa.Column("last_name", sa.String(length=15), nullable=True, default=None),
    sa.Column("user_email", sa.String(length=60), nullable=False, unique=True),
    sa.Column(
        "hashed_password", sa.String(length=256), nullable=True, default=None
    ),
    sa.Column("is_active", sa.Boolean(), nullable=False, default=False),
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


def map_users_table() -> None:
    mapper_registry.map_imperatively(
        User,
        users_table,
        properties={
            "company": relationship(
                "Company", back_populates="user", cascade="all, delete-orphan"
            ),
            "company_user": relationship(
                "CompanyUser",
                back_populates="user",
                cascade="all, delete-orphan",
            ),
            "full_name": composite(
                FullName, users_table.c.first_name, users_table.c.last_name
            ),
            "email": composite(UserEmail, users_table.c.user_email),
        },
    )

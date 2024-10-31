import sqlalchemy as sa
from sqlalchemy.orm import composite, relationship

from app.core.entities.company import (
    Company,
    Visibility,
)
from app.core.entities.value_objects import CompanyDescription, CompanyName

from .base import mapper_registry

companies_table = sa.Table(
    "companies",
    mapper_registry.metadata,
    sa.Column(
        "company_id",
        sa.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    ),
    sa.Column(
        "owner_id",
        sa.Integer,
        sa.ForeignKey("users.user_id", ondelete="CASCADE"),
    ),
    sa.Column("company_name", sa.String(length=15), nullable=False),
    sa.Column(
        "company_description",
        sa.String(length=128),
        nullable=True,
        default=None,
    ),
    sa.Column("visibility", sa.Enum(Visibility), default=Visibility.VISIBLE),
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


def map_companies_table() -> None:
    mapper_registry.map_imperatively(
        Company,
        companies_table,
        properties={
            "user": relationship("User", back_populates="company"),
            "company_user": relationship(
                "CompanyUser",
                back_populates="company",
                cascade="all, delete-orphan",
            ),
            "invitation": relationship(
                "Invitation",
                back_populates="company",
                cascade="all, delete-orphan",
            ),
            "user_request": relationship(
                "UserRequest",
                back_populates="company",
                cascade="all, delete-orphan",
            ),
            "name": composite(CompanyName, companies_table.c.company_name),
            "description": composite(
                CompanyDescription, companies_table.c.company_description
            ),
        },
    )

"""invite tables

Revision ID: 209907698680
Revises: 39ba5639f2c2
Create Date: 2024-10-31 21:32:19.261695

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "209907698680"
down_revision: Union[str, None] = "39ba5639f2c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "invitations",
        sa.Column(
            "invitation_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column(
            "status",
            sa.Enum("NEW", "ACCEPTED", "REJECTED", name="requeststatus"),
            nullable=True,
        ),
        sa.Column("company_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.company_id"],
            name=op.f("fk_invitations_company_id_companies"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.user_id"],
            name=op.f("fk_invitations_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("invitation_id", name=op.f("pk_invitations")),
        sa.UniqueConstraint(
            "invitation_id", name=op.f("uq_invitations_invitation_id")
        ),
    )
    op.create_table(
        "user_requests",
        sa.Column(
            "user_request_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column(
            "status",
            sa.Enum("NEW", "ACCEPTED", "REJECTED", name="requeststatus"),
            nullable=True,
        ),
        sa.Column("company_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.company_id"],
            name=op.f("fk_user_requests_company_id_companies"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.user_id"],
            name=op.f("fk_user_requests_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "user_request_id", name=op.f("pk_user_requests")
        ),
        sa.UniqueConstraint(
            "user_request_id", name=op.f("uq_user_requests_user_request_id")
        ),
    )
    op.create_unique_constraint(
        op.f("uq_companies_company_id"), "companies", ["company_id"]
    )
    op.create_unique_constraint(
        op.f("uq_company_users_company_user_id"),
        "company_users",
        ["company_user_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("uq_company_users_company_user_id"),
        "company_users",
        type_="unique",
    )
    op.drop_constraint(
        op.f("uq_companies_company_id"), "companies", type_="unique"
    )
    op.drop_table("user_requests")
    op.drop_table("invitations")

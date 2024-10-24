"""user model

Revision ID: 066cc787045a
Revises:
Create Date: 2024-10-23 15:12:51.651594

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "066cc787045a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("first_name", sa.String(length=15), nullable=False),
        sa.Column("last_name", sa.String(length=15), nullable=False),
        sa.Column("user_email", sa.String(length=60), nullable=False),
        sa.Column("hashed_password", sa.String(length=256), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
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
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_users")),
        sa.UniqueConstraint("user_email", name=op.f("uq_users_user_email")),
        sa.UniqueConstraint("user_id", name=op.f("uq_users_user_id")),
    )


def downgrade() -> None:
    op.drop_table("users")

"""user table

Revision ID: 854837fa6628
Revises:
Create Date: 2024-10-27 21:14:35.758396

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "854837fa6628"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("first_name", sa.String(length=15), nullable=True),
        sa.Column("last_name", sa.String(length=15), nullable=True),
        sa.Column("user_email", sa.String(length=60), nullable=False),
        sa.Column("hashed_password", sa.String(length=256), nullable=True),
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

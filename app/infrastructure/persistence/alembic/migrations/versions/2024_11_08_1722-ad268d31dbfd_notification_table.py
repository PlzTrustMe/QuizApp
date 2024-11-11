"""notification table

Revision ID: ad268d31dbfd
Revises: aac1c5be1180
Create Date: 2024-11-08 17:22:28.181200

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ad268d31dbfd"
down_revision: Union[str, None] = "aac1c5be1180"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notifications",
        sa.Column(
            "notification_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column("send_to", sa.Integer(), nullable=True),
        sa.Column("text", sa.String(length=128), nullable=False),
        sa.Column(
            "status",
            sa.Enum("NEW", "READ", name="notificationstatus"),
            nullable=True,
        ),
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
            ["send_to"],
            ["company_users.company_user_id"],
            name=op.f("fk_notifications_send_to_company_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "notification_id", name=op.f("pk_notifications")
        ),
        sa.UniqueConstraint(
            "notification_id", name=op.f("uq_notifications_notification_id")
        ),
    )
    op.create_unique_constraint(
        op.f("uq_quiz_participations_quiz_participation_id"),
        "quiz_participations",
        ["quiz_participation_id"],
    )
    op.create_unique_constraint(
        op.f("uq_quiz_results_quiz_result_id"),
        "quiz_results",
        ["quiz_result_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("uq_quiz_results_quiz_result_id"), "quiz_results", type_="unique"
    )
    op.drop_constraint(
        op.f("uq_quiz_participations_quiz_participation_id"),
        "quiz_participations",
        type_="unique",
    )
    op.drop_table("notifications")

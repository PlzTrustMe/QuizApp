"""quiz tables

Revision ID: 3edb5634185d
Revises: 209907698680
Create Date: 2024-11-04 14:59:16.860214

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3edb5634185d"
down_revision: Union[str, None] = "209907698680"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "quizzes",
        sa.Column("quiz_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=122), nullable=False),
        sa.Column("description", sa.String(length=122), nullable=False),
        sa.Column("participation_count", sa.Integer(), nullable=False),
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
            name=op.f("fk_quizzes_company_id_companies"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("quiz_id", name=op.f("pk_quizzes")),
        sa.UniqueConstraint("quiz_id", name=op.f("uq_quizzes_quiz_id")),
    )
    op.create_table(
        "questions",
        sa.Column(
            "question_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column("quiz_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=122), nullable=False),
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
            ["quiz_id"],
            ["quizzes.quiz_id"],
            name=op.f("fk_questions_quiz_id_quizzes"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("question_id", name=op.f("pk_questions")),
        sa.UniqueConstraint(
            "question_id", name=op.f("uq_questions_question_id")
        ),
    )
    op.create_table(
        "answers",
        sa.Column(
            "answer_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column("question_id", sa.Integer(), nullable=True),
        sa.Column("text", sa.String(length=122), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=True),
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
            ["question_id"],
            ["questions.question_id"],
            name=op.f("fk_answers_question_id_questions"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("answer_id", name=op.f("pk_answers")),
        sa.UniqueConstraint("answer_id", name=op.f("uq_answers_answer_id")),
    )
    op.create_unique_constraint(
        op.f("uq_invitations_invitation_id"), "invitations", ["invitation_id"]
    )
    op.create_unique_constraint(
        op.f("uq_user_requests_user_request_id"),
        "user_requests",
        ["user_request_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("uq_user_requests_user_request_id"),
        "user_requests",
        type_="unique",
    )
    op.drop_constraint(
        op.f("uq_invitations_invitation_id"), "invitations", type_="unique"
    )
    op.drop_table("answers")
    op.drop_table("questions")
    op.drop_table("quizzes")

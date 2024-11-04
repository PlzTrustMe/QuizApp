"""quiz result tables

Revision ID: aac1c5be1180
Revises: 3edb5634185d
Create Date: 2024-11-04 23:07:19.096002

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aac1c5be1180"
down_revision: Union[str, None] = "3edb5634185d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "quiz_participations",
        sa.Column(
            "quiz_participation_id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("quiz_id", sa.Integer(), nullable=True),
        sa.Column("company_user_id", sa.Integer(), nullable=True),
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
            ["company_user_id"],
            ["company_users.company_user_id"],
            name=op.f("fk_quiz_participations_company_user_id_company_users"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["quiz_id"],
            ["quizzes.quiz_id"],
            name=op.f("fk_quiz_participations_quiz_id_quizzes"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "quiz_participation_id", name=op.f("pk_quiz_participations")
        ),
        sa.UniqueConstraint(
            "quiz_participation_id",
            name=op.f("uq_quiz_participations_quiz_participation_id"),
        ),
    )
    op.create_table(
        "quiz_results",
        sa.Column(
            "quiz_result_id", sa.Integer(), autoincrement=True, nullable=False
        ),
        sa.Column("quiz_participation_id", sa.Integer(), nullable=True),
        sa.Column("correct_answers", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["quiz_participation_id"],
            ["quiz_participations.quiz_participation_id"],
            name=op.f(
                "fk_quiz_results_quiz_participation_id_quiz_participations"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "quiz_result_id", name=op.f("pk_quiz_results")
        ),
        sa.UniqueConstraint(
            "quiz_result_id", name=op.f("uq_quiz_results_quiz_result_id")
        ),
    )
    op.create_unique_constraint(
        op.f("uq_answers_answer_id"), "answers", ["answer_id"]
    )
    op.create_unique_constraint(
        op.f("uq_questions_question_id"), "questions", ["question_id"]
    )
    op.create_unique_constraint(
        op.f("uq_quizzes_quiz_id"), "quizzes", ["quiz_id"]
    )


def downgrade() -> None:
    op.drop_constraint(op.f("uq_quizzes_quiz_id"), "quizzes", type_="unique")
    op.drop_constraint(
        op.f("uq_questions_question_id"), "questions", type_="unique"
    )
    op.drop_constraint(op.f("uq_answers_answer_id"), "answers", type_="unique")
    op.drop_table("quiz_results")
    op.drop_table("quiz_participations")

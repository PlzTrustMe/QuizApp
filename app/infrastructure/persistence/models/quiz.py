import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.core.entities.quiz import Answer, Question, Quiz

from .base import mapper_registry

quizzes_table = sa.Table(
    "quizzes",
    mapper_registry.metadata,
    sa.Column(
        "quiz_id",
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
    sa.Column("title", sa.String(length=122), nullable=False),
    sa.Column("description", sa.String(length=122), nullable=False),
    sa.Column("participation_count", sa.Integer, default=0, nullable=False),
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

questions_table = sa.Table(
    "questions",
    mapper_registry.metadata,
    sa.Column(
        "question_id",
        sa.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    ),
    sa.Column(
        "quiz_id",
        sa.Integer,
        sa.ForeignKey("quizzes.quiz_id", ondelete="CASCADE"),
    ),
    sa.Column("title", sa.String(length=122), nullable=False),
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

answers_table = sa.Table(
    "answers",
    mapper_registry.metadata,
    sa.Column(
        "answer_id",
        sa.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    ),
    sa.Column(
        "question_id",
        sa.Integer,
        sa.ForeignKey("questions.question_id", ondelete="CASCADE"),
    ),
    sa.Column("text", sa.String(length=122), nullable=False),
    sa.Column("is_correct", sa.Boolean, default=False),
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


def map_quizzes_table() -> None:
    mapper_registry.map_imperatively(
        Quiz,
        quizzes_table,
        properties={
            "company": relationship("Company", back_populates="quiz"),
            "question": relationship(
                "Question", back_populates="quiz", cascade="all, delete-orphan"
            ),
        },
    )


def map_questions_table() -> None:
    mapper_registry.map_imperatively(
        Question,
        questions_table,
        properties={
            "quiz": relationship("Quiz", back_populates="question"),
            "answer": relationship(
                "Answer",
                back_populates="question",
                cascade="all, delete-orphan",
            ),
        },
    )


def map_answers_table() -> None:
    mapper_registry.map_imperatively(
        Answer,
        answers_table,
        properties={
            "question": relationship("Question", back_populates="answer")
        },
    )

"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-08-10

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    session_status = sa.Enum(
        "in_progress",
        "completed",
        "abandoned",
        name="session_status",
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("first_name", sa.String(length=128), nullable=True),
        sa.Column("language", sa.String(length=8), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column(
            "last_active_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    op.create_index(
        "ix_users_telegram_id",
        "users",
        ["telegram_id"],
        unique=True,
    )

    op.create_table(
        "test_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "status",
            session_status,
            nullable=False,
            server_default="in_progress",
        ),
    )

    op.create_index(
        "ix_test_sessions_user_id",
        "test_sessions",
        ["user_id"],
    )

    op.create_index(
        "ix_test_sessions_user_status",
        "test_sessions",
        ["user_id", "status"],
    )

    op.create_table(
        "test_answers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "session_id",
            sa.Integer(),
            sa.ForeignKey("test_sessions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("question_number", sa.Integer(), nullable=False),
        sa.Column("answer_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint(
            "session_id",
            "question_number",
            name="uq_session_question",
        ),
    )

    op.create_index(
        "ix_test_answers_session_id",
        "test_answers",
        ["session_id"],
    )

    op.create_table(
        "test_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "session_id",
            sa.Integer(),
            sa.ForeignKey("test_sessions.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("mbti_type", sa.String(length=4), nullable=False),
        sa.Column("e_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("i_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("s_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("n_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("t_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("f_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("j_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("p_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    op.create_index(
        "ix_test_results_user_id",
        "test_results",
        ["user_id"],
    )

    op.create_index(
        "ix_test_results_mbti_type",
        "test_results",
        ["mbti_type"],
    )

    op.create_index(
        "ix_test_results_created_at",
        "test_results",
        ["created_at"],
    )

    op.create_table(
        "statistic_sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("source_url", sa.String(length=512), nullable=True),
        sa.Column("publication_year", sa.String(length=32), nullable=True),
        sa.Column("population", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("data", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    op.create_index(
        "ix_statistic_sources_category",
        "statistic_sources",
        ["category"],
    )


def downgrade() -> None:
    op.drop_table("statistic_sources")
    op.drop_table("test_results")
    op.drop_table("test_answers")
    op.drop_table("test_sessions")
    op.drop_table("users")

    sa.Enum(
        "in_progress",
        "completed",
        "abandoned",
        name="session_status",
    ).drop(op.get_bind(), checkfirst=True)
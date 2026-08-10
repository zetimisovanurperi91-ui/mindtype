from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Index, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class SessionStatus(str, enum.Enum):
    in_progress = "in_progress"
    completed = "completed"
    abandoned = "abandoned"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    language: Mapped[str | None] = mapped_column(String(8), nullable=True)  # "en" | "ru" | None until chosen
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_active_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    sessions: Mapped[list["TestSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    results: Mapped[list["TestResult"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<User id={self.id} tg={self.telegram_id} lang={self.language}>"


class TestSession(Base):
    __tablename__ = "test_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus, name="session_status"), default=SessionStatus.in_progress, nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="sessions")
    answers: Mapped[list["TestAnswer"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    result: Mapped["TestResult | None"] = relationship(back_populates="session", uselist=False)

    __table_args__ = (Index("ix_test_sessions_user_status", "user_id", "status"),)


class TestAnswer(Base):
    __tablename__ = "test_answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("test_sessions.id", ondelete="CASCADE"), index=True, nullable=False)
    question_number: Mapped[int] = mapped_column(nullable=False)
    answer_id: Mapped[int] = mapped_column(nullable=False)  # index of chosen option within the question
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["TestSession"] = relationship(back_populates="answers")

    __table_args__ = (
        UniqueConstraint("session_id", "question_number", name="uq_session_question"),
    )


class TestResult(Base):
    __tablename__ = "test_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("test_sessions.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    mbti_type: Mapped[str] = mapped_column(String(4), index=True, nullable=False)

    e_score: Mapped[int] = mapped_column(default=0)
    i_score: Mapped[int] = mapped_column(default=0)
    s_score: Mapped[int] = mapped_column(default=0)
    n_score: Mapped[int] = mapped_column(default=0)
    t_score: Mapped[int] = mapped_column(default=0)
    f_score: Mapped[int] = mapped_column(default=0)
    j_score: Mapped[int] = mapped_column(default=0)
    p_score: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    user: Mapped["User"] = relationship(back_populates="results")
    session: Mapped["TestSession"] = relationship(back_populates="result")


class StatisticSource(Base):
    """Curated, citeable research statistics. Seeded from app/data/sources.py,
    never user-editable through the bot. See statistics_service.py for how
    this is kept separate from live bot-derived statistics."""

    __tablename__ = "statistic_sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    publication_year: Mapped[str | None] = mapped_column(String(32), nullable=True)
    population: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    data: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON-encoded figure(s)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

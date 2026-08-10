from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import SessionStatus, TestResult, TestSession, User


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class StatsRepository:
    """All queries here compute LIVE numbers from the database - nothing is
    hardcoded or cached as a fixed percentage. These are always rendered
    under a "MindType users" / bot-statistics label, never presented as
    global population data (see statistics_service.py)."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def total_users(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(User))
        return result.scalar_one()

    async def total_completed_tests(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(TestResult))
        return result.scalar_one()

    async def tests_since(self, since: datetime) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(TestResult).where(TestResult.created_at >= since)
        )
        return result.scalar_one()

    async def users_since(self, since: datetime) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(User).where(User.created_at >= since)
        )
        return result.scalar_one()

    async def sessions_started_total(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(TestSession))
        return result.scalar_one()

    async def mbti_type_distribution(self) -> dict[str, int]:
        result = await self.session.execute(
            select(TestResult.mbti_type, func.count()).group_by(TestResult.mbti_type)
        )
        return dict(result.all())

    async def axis_letter_counts(self) -> dict[str, int]:
        """Sums how many completed results have each *winning* letter, derived
        straight from the stored mbti_type string - no separate bookkeeping
        needed, and it can never drift from the actual results."""
        distribution = await self.mbti_type_distribution()
        letters = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        for mbti_type, count in distribution.items():
            for letter in mbti_type:
                if letter in letters:
                    letters[letter] += count
        return letters

    async def language_breakdown(self) -> dict[str, dict[str, int]]:
        """Returns {"en": {"users": N, "completed": M}, "ru": {...}}"""
        users_q = await self.session.execute(select(User.language, func.count()).group_by(User.language))
        users_by_lang = {lang or "unset": count for lang, count in users_q.all()}

        completed_q = await self.session.execute(
            select(User.language, func.count(TestResult.id))
            .join(TestResult, TestResult.user_id == User.id)
            .group_by(User.language)
        )
        completed_by_lang = {lang or "unset": count for lang, count in completed_q.all()}

        breakdown: dict[str, dict[str, int]] = {}
        for lang in set(users_by_lang) | set(completed_by_lang):
            breakdown[lang] = {
                "users": users_by_lang.get(lang, 0),
                "completed": completed_by_lang.get(lang, 0),
            }
        return breakdown

    async def activity_window(self) -> dict[str, dict[str, int]]:
        now = _utc_now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        last_7 = now - timedelta(days=7)
        last_30 = now - timedelta(days=30)

        async def window(start: datetime, end: datetime | None = None) -> dict[str, int]:
            user_stmt = select(func.count()).select_from(User).where(User.created_at >= start)
            test_stmt = select(func.count()).select_from(TestResult).where(TestResult.created_at >= start)
            if end is not None:
                user_stmt = user_stmt.where(User.created_at < end)
                test_stmt = test_stmt.where(TestResult.created_at < end)
            users = (await self.session.execute(user_stmt)).scalar_one()
            tests = (await self.session.execute(test_stmt)).scalar_one()
            return {"new_users": users, "completed_tests": tests}

        return {
            "today": await window(today_start),
            "yesterday": await window(yesterday_start, today_start),
            "last_7_days": await window(last_7),
            "last_30_days": await window(last_30),
        }

    async def export_rows(self) -> list[dict]:
        """Non-sensitive analytics rows for CSV export - no raw usernames
        beyond what's already in the User table, no private message content."""
        stmt = (
            select(
                User.telegram_id,
                User.language,
                TestResult.mbti_type,
                TestResult.e_score,
                TestResult.i_score,
                TestResult.s_score,
                TestResult.n_score,
                TestResult.t_score,
                TestResult.f_score,
                TestResult.j_score,
                TestResult.p_score,
                TestResult.created_at,
            )
            .join(TestResult, TestResult.user_id == User.id)
            .order_by(TestResult.created_at.desc())
        )
        result = await self.session.execute(stmt)
        rows = []
        for row in result.all():
            rows.append(
                {
                    "telegram_id": row.telegram_id,
                    "language": row.language,
                    "mbti_type": row.mbti_type,
                    "e_score": row.e_score,
                    "i_score": row.i_score,
                    "s_score": row.s_score,
                    "n_score": row.n_score,
                    "t_score": row.t_score,
                    "f_score": row.f_score,
                    "j_score": row.j_score,
                    "p_score": row.p_score,
                    "created_at": row.created_at.isoformat() if row.created_at else "",
                }
            )
        return rows

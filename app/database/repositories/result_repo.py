from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import TestResult
from app.services.mbti_engine import MBTIResult


class ResultRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_result(self, user_id: int, session_id: int, result: MBTIResult) -> TestResult:
        raw = result.raw_scores
        test_result = TestResult(
            user_id=user_id,
            session_id=session_id,
            mbti_type=result.mbti_type,
            e_score=raw.get("E", 0),
            i_score=raw.get("I", 0),
            s_score=raw.get("S", 0),
            n_score=raw.get("N", 0),
            t_score=raw.get("T", 0),
            f_score=raw.get("F", 0),
            j_score=raw.get("J", 0),
            p_score=raw.get("P", 0),
        )
        self.session.add(test_result)
        await self.session.commit()
        await self.session.refresh(test_result)
        return test_result

    async def get_latest_for_user(self, user_id: int) -> TestResult | None:
        # Order by id as a tiebreaker: two results can share the same
        # server-generated timestamp (e.g. within the same second), and we
        # always want the most recently *created* row, not an arbitrary one.
        result = await self.session.execute(
            select(TestResult)
            .where(TestResult.user_id == user_id)
            .order_by(TestResult.created_at.desc(), TestResult.id.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_by_id_for_user(self, result_id: int, user_id: int) -> TestResult | None:
        """Ownership-checked lookup - a user can never load another user's
        result by guessing/replaying an id in callback data."""
        result = await self.session.execute(
            select(TestResult).where(TestResult.id == result_id, TestResult.user_id == user_id)
        )
        return result.scalar_one_or_none()

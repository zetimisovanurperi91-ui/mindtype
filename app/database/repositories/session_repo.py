from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models import SessionStatus, TestAnswer, TestSession


class SessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_active_session(self, user_id: int) -> TestSession | None:
        result = await self.session.execute(
            select(TestSession)
            .options(selectinload(TestSession.answers))
            .where(TestSession.user_id == user_id, TestSession.status == SessionStatus.in_progress)
            .order_by(TestSession.started_at.desc())
        )
        return result.scalars().first()

    async def get_by_id(self, session_id: int) -> TestSession | None:
        result = await self.session.execute(
            select(TestSession).options(selectinload(TestSession.answers)).where(TestSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def create_session(self, user_id: int) -> TestSession:
        test_session = TestSession(user_id=user_id, status=SessionStatus.in_progress)
        self.session.add(test_session)
        await self.session.commit()
        await self.session.refresh(test_session)
        return test_session

    async def abandon_session(self, test_session: TestSession) -> None:
        test_session.status = SessionStatus.abandoned
        await self.session.commit()

    async def complete_session(self, test_session: TestSession) -> None:
        from sqlalchemy import func

        test_session.status = SessionStatus.completed
        test_session.completed_at = func.now()  # type: ignore[assignment]
        await self.session.commit()

    async def save_answer(self, session_id: int, question_number: int, answer_id: int) -> None:
        answer = TestAnswer(session_id=session_id, question_number=question_number, answer_id=answer_id)
        self.session.add(answer)
        await self.session.commit()

    async def get_answers(self, session_id: int) -> list[TestAnswer]:
        result = await self.session.execute(
            select(TestAnswer).where(TestAnswer.session_id == session_id).order_by(TestAnswer.question_number)
        )
        return list(result.scalars().all())

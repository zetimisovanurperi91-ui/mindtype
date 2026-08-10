from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

    async def get_or_create(
        self, telegram_id: int, username: str | None, first_name: str | None
    ) -> tuple[User, bool]:
        """Returns (user, created)."""
        user = await self.get_by_telegram_id(telegram_id)
        if user is not None:
            # keep username/first_name reasonably fresh
            user.username = username
            user.first_name = first_name
            await self.session.commit()
            return user, False

        user = User(telegram_id=telegram_id, username=username, first_name=first_name)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user, True

    async def set_language(self, user: User, language: str) -> None:
        user.language = language
        await self.session.commit()

    async def touch_activity(self, user: User) -> None:
        user.last_active_at = func.now()  # type: ignore[assignment]
        await self.session.commit()

    async def count_total(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(User))
        return result.scalar_one()

    async def count_by_language(self) -> dict[str, int]:
        result = await self.session.execute(select(User.language, func.count()).group_by(User.language))
        return {lang or "unset": count for lang, count in result.all()}

    async def count_created_since(self, since) -> int:
        result = await self.session.execute(select(func.count()).select_from(User).where(User.created_at >= since))
        return result.scalar_one()

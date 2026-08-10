from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from app.database.repositories.user_repo import UserRepository
from app.database.session import async_session_factory

logger = logging.getLogger(__name__)


class DbSessionMiddleware(BaseMiddleware):
    """Opens one AsyncSession per update, resolves/creates the acting User,
    and injects `session` and `user` into handler kwargs. Handlers should
    never open their own sessions - this keeps transaction scope predictable
    and means every handler automatically has an up-to-date User row.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        telegram_user = data.get("event_from_user")
        if telegram_user is None:
            return await handler(event, data)

        async with async_session_factory() as session:
            repo = UserRepository(session)
            try:
                user, _created = await repo.get_or_create(
                    telegram_id=telegram_user.id,
                    username=telegram_user.username,
                    first_name=telegram_user.first_name,
                )
                await repo.touch_activity(user)
            except Exception:  # pragma: no cover - defensive, DB hiccups shouldn't crash the bot
                logger.exception("Failed to resolve user for telegram_id=%s", telegram_user.id)
                raise

            data["session"] = session
            data["user"] = user
            return await handler(event, data)

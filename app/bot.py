from __future__ import annotations

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError
from aiogram.types import ErrorEvent

from app.config import settings
from app.handlers import get_root_router
from app.middlewares import DbSessionMiddleware
from app.services.localization import preload_all

logger = logging.getLogger(__name__)


def create_bot() -> Bot:
    return Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.update.middleware(DbSessionMiddleware())
    dispatcher.include_router(get_root_router())

    @dispatcher.error()
    async def on_error(event: ErrorEvent) -> bool:
        # Catch-all so a bad callback, a stale button, or a transient DB
        # error never crashes the whole polling loop.
        if isinstance(event.exception, TelegramAPIError):
            logger.warning("Telegram API error: %s", event.exception)
        else:
            logger.exception("Unhandled error while processing update", exc_info=event.exception)
        return True

    preload_all()
    return dispatcher

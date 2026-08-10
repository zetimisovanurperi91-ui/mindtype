from __future__ import annotations

import asyncio
import logging

from alembic import command
from alembic.config import Config

from app.bot import create_bot, create_dispatcher


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("mindtype")


def run_migrations() -> None:
    """Apply all pending Alembic migrations before starting the bot."""
    logger.info("Applying database migrations...")

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    logger.info("Migrations applied.")


async def main() -> None:
    bot = create_bot()
    dispatcher = create_dispatcher()

    logger.info("MindType bot starting...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    run_migrations()
    asyncio.run(main())
from aiogram import Router

from app.handlers import admin, result, start, statistics, test


def get_root_router() -> Router:
    root = Router(name="root")
    # Admin routes first so `/admin` and admin callbacks are matched before
    # any broader catch-alls; order otherwise doesn't matter since every
    # handler filters on specific commands/callback_data prefixes.
    root.include_router(admin.router)
    root.include_router(start.router)
    root.include_router(test.router)
    root.include_router(result.router)
    root.include_router(statistics.router)
    return root

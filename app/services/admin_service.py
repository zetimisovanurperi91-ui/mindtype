from __future__ import annotations

from app.config import settings


def is_admin(telegram_id: int) -> bool:
    """The ONLY place admin identity is decided. Handlers and keyboard
    builders must call this rather than re-implementing the check, so a
    change to ADMIN_IDS never needs to be hunted down across the codebase."""
    return telegram_id in settings.admin_id_set

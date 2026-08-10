from __future__ import annotations

from aiogram.types import CallbackQuery, Message

from app.database.models import User
from app.keyboards.user import main_menu_keyboard
from app.services.localization import t


async def send_main_menu(target: Message | CallbackQuery, user: User) -> None:
    text = t(user.language, "menu.title")
    keyboard = main_menu_keyboard(user.language, user.telegram_id)

    if isinstance(target, CallbackQuery):
        message = target.message
        if message is not None:
            try:
                await message.edit_text(text, reply_markup=keyboard)
                return
            except Exception:
                # message too old / not modified / not editable -> fall back to sending a new one
                await message.answer(text, reply_markup=keyboard)
                return
    else:
        await target.answer(text, reply_markup=keyboard)

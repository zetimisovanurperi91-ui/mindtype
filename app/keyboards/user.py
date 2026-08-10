from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.services.admin_service import is_admin
from app.services.localization import t


def main_menu_keyboard(language: str, telegram_id: int) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=t(language, "menu.take_test"), callback_data="menu:test")],
        [InlineKeyboardButton(text=t(language, "menu.my_result"), callback_data="menu:result")],
        [InlineKeyboardButton(text=t(language, "menu.statistics"), callback_data="menu:stats")],
        [InlineKeyboardButton(text=t(language, "menu.about"), callback_data="menu:about")],
        [InlineKeyboardButton(text=t(language, "menu.change_language"), callback_data="menu:change_lang")],
    ]
    if is_admin(telegram_id):
        rows.append([InlineKeyboardButton(text=t(language, "menu.admin_panel"), callback_data="admin:open")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def resume_test_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(language, "test.resume_continue"), callback_data="test:resume")],
            [InlineKeyboardButton(text=t(language, "test.resume_restart"), callback_data="test:restart")],
        ]
    )


def back_to_menu_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="◀️ " + t(language, "menu.title"), callback_data="menu:open")]]
    )

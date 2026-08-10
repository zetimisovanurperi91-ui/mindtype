from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.services.localization import t


def admin_panel_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(language, "admin.btn_overview"), callback_data="admin:overview")],
            [InlineKeyboardButton(text=t(language, "admin.btn_distribution"), callback_data="admin:distribution")],
            [InlineKeyboardButton(text=t(language, "admin.btn_dimensions"), callback_data="admin:dimensions")],
            [InlineKeyboardButton(text=t(language, "admin.btn_languages"), callback_data="admin:languages")],
            [InlineKeyboardButton(text=t(language, "admin.btn_export"), callback_data="admin:export")],
            [InlineKeyboardButton(text=t(language, "admin.btn_refresh"), callback_data="admin:open")],
            [InlineKeyboardButton(text="◀️ " + t(language, "menu.title"), callback_data="menu:open")],
        ]
    )

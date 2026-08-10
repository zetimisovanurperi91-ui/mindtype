from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.services.localization import t


def statistics_menu_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(language, "stats.menu_types"), callback_data="stats:types")],
            [InlineKeyboardButton(text=t(language, "stats.menu_ei"), callback_data="stats:axis:EI")],
            [InlineKeyboardButton(text=t(language, "stats.menu_sn"), callback_data="stats:axis:SN")],
            [InlineKeyboardButton(text=t(language, "stats.menu_tf"), callback_data="stats:axis:TF")],
            [InlineKeyboardButton(text=t(language, "stats.menu_jp"), callback_data="stats:axis:JP")],
            [InlineKeyboardButton(text="◀️ " + t(language, "menu.title"), callback_data="menu:open")],
        ]
    )

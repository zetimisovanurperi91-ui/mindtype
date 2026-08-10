from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.database.repositories.session_repo import SessionRepository
from app.database.repositories.user_repo import UserRepository
from app.handlers.common import send_main_menu
from app.keyboards.language import language_keyboard
from app.keyboards.user import back_to_menu_keyboard, resume_test_keyboard
from app.services.localization import t

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, user: User) -> None:
    if user.language is None:
        await message.answer(
            f"{t(None, 'welcome.title')}\n{t(None, 'welcome.subtitle')}\n\n{t(None, 'welcome.choose_language')}",
            reply_markup=language_keyboard(),
        )
        return

    active = await SessionRepository(session).get_active_session(user.id)
    if active is not None:
        await message.answer(t(user.language, "test.resume_prompt"), reply_markup=resume_test_keyboard(user.language))
        return

    await send_main_menu(message, user)


@router.callback_query(F.data.startswith("lang:"))
async def on_language_chosen(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    language = callback.data.split(":", 1)[1]
    await UserRepository(session).set_language(user, language)
    user.language = language  # keep the in-memory object consistent for the rest of this update

    if callback.message is not None:
        await callback.message.edit_text(t(language, "language.saved"))
    await send_main_menu(callback, user)
    await callback.answer()


@router.callback_query(F.data == "menu:change_lang")
async def on_change_language(callback: CallbackQuery, user: User) -> None:
    if callback.message is not None:
        await callback.message.edit_text(t(user.language, "welcome.choose_language"), reply_markup=language_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:open")
async def on_menu_open(callback: CallbackQuery, user: User) -> None:
    await send_main_menu(callback, user)
    await callback.answer()


@router.callback_query(F.data == "menu:about")
async def on_about(callback: CallbackQuery, user: User) -> None:
    if callback.message is not None:
        await callback.message.edit_text(t(user.language, "about.text"), reply_markup=back_to_menu_keyboard(user.language))
    await callback.answer()

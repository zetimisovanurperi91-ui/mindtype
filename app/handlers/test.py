from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.questions import TOTAL_QUESTIONS, get_question
from app.database.models import TestSession, User
from app.database.repositories.result_repo import ResultRepository
from app.database.repositories.session_repo import SessionRepository
from app.handlers.result import render_result
from app.keyboards.test import question_keyboard
from app.services.localization import t
from app.services.mbti_engine import score_answers

router = Router(name="test")
logger = logging.getLogger(__name__)


def _progress_bar(current: int, total: int, length: int = 15) -> str:
    filled = round(current / total * length)
    filled = max(0, min(length, filled))
    return "█" * filled + "░" * (length - filled)


async def _render_question(callback_or_message, user: User, test_session: TestSession, question_number: int) -> None:
    question = get_question(question_number)
    if question is None:  # shouldn't happen, defensive guard
        return

    header = t(user.language, "test.question_progress", current=question_number, total=TOTAL_QUESTIONS)
    bar = _progress_bar(question_number, TOTAL_QUESTIONS)
    question_text = question["text"].get(user.language, question["text"]["en"])
    text = f"{header}\n{bar}\n\n{question_text}"
    keyboard = question_keyboard(question, test_session.id, user.language)

    message = callback_or_message.message if isinstance(callback_or_message, CallbackQuery) else callback_or_message
    if message is None:
        return
    try:
        await message.edit_text(text, reply_markup=keyboard)
    except Exception:
        await message.answer(text, reply_markup=keyboard)


async def _next_question_number(session: AsyncSession, test_session: TestSession) -> int:
    answers = await SessionRepository(session).get_answers(test_session.id)
    return len(answers) + 1


async def _start_fresh_session(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    repo = SessionRepository(session)
    existing = await repo.get_active_session(user.id)
    if existing is not None:
        await repo.abandon_session(existing)
    test_session = await repo.create_session(user.id)
    await _render_question(callback, user, test_session, 1)


@router.callback_query(F.data == "menu:test")
async def on_take_test(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    repo = SessionRepository(session)
    active = await repo.get_active_session(user.id)
    if active is not None:
        next_number = await _next_question_number(session, active)
        await _render_question(callback, user, active, next_number)
    else:
        await _start_fresh_session(callback, session, user)
    await callback.answer()


@router.callback_query(F.data == "test:resume")
async def on_resume(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    repo = SessionRepository(session)
    active = await repo.get_active_session(user.id)
    if active is None:
        await _start_fresh_session(callback, session, user)
    else:
        next_number = await _next_question_number(session, active)
        await _render_question(callback, user, active, next_number)
    await callback.answer()


@router.callback_query(F.data == "test:restart")
async def on_restart(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    await _start_fresh_session(callback, session, user)
    await callback.answer()


@router.callback_query(F.data.startswith("ans:"))
async def on_answer(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    try:
        _, session_id_str, question_id_str, option_index_str = callback.data.split(":")
        session_id, question_id, option_index = int(session_id_str), int(question_id_str), int(option_index_str)
    except (ValueError, AttributeError):
        await callback.answer(t(user.language, "errors.stale_button"), show_alert=True)
        return

    repo = SessionRepository(session)
    test_session = await repo.get_by_id(session_id)

    # Ownership + validity checks - never trust callback data at face value.
    if test_session is None or test_session.user_id != user.id:
        await callback.answer(t(user.language, "errors.not_your_session"), show_alert=True)
        return
    if test_session.status.value != "in_progress":
        await callback.answer(t(user.language, "errors.stale_button"), show_alert=True)
        return

    expected_question_number = await _next_question_number(session, test_session)
    if question_id != expected_question_number:
        # User tapped an old/duplicate question's button (e.g. double-tap,
        # or pressed Back on Telegram to an earlier message).
        await callback.answer(t(user.language, "errors.stale_button"), show_alert=True)
        return

    question = get_question(question_id)
    if question is None or not (0 <= option_index < len(question["options"])):
        await callback.answer(t(user.language, "errors.stale_button"), show_alert=True)
        return

    await repo.save_answer(session_id, question_id, option_index)
    await callback.answer()

    if question_id == TOTAL_QUESTIONS:
        await _finish_test(callback, session, user, test_session)
    else:
        await _render_question(callback, user, test_session, question_id + 1)


async def _finish_test(callback: CallbackQuery, session: AsyncSession, user: User, test_session: TestSession) -> None:
    session_repo = SessionRepository(session)
    answers = await session_repo.get_answers(test_session.id)

    answer_weights: dict[int, dict[str, int]] = {}
    for answer in answers:
        question = get_question(answer.question_number)
        if question is None:
            continue
        answer_weights[answer.question_number] = question["options"][answer.answer_id]["weights"]

    result = score_answers(answer_weights)

    if callback.message is not None:
        try:
            await callback.message.edit_text(t(user.language, "test.completed_processing"))
        except Exception:
            pass

    await session_repo.complete_session(test_session)
    test_result = await ResultRepository(session).save_result(user.id, test_session.id, result)

    await render_result(callback, user, session, test_result)

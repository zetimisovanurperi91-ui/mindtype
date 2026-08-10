from __future__ import annotations

import csv
import io
from datetime import datetime, timezone

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.database.repositories.stats_repo import StatsRepository
from app.keyboards.admin import admin_panel_keyboard
from app.services.admin_service import is_admin
from app.services.localization import t

router = Router(name="admin")


async def _edit_or_send(target: Message | CallbackQuery, text: str, keyboard) -> None:
    if isinstance(target, CallbackQuery):
        if target.message is not None:
            try:
                await target.message.edit_text(text, reply_markup=keyboard)
            except Exception:
                await target.message.answer(text, reply_markup=keyboard)
    else:
        await target.answer(text, reply_markup=keyboard)


@router.message(Command("admin"))
async def cmd_admin(message: Message, user: User) -> None:
    if not is_admin(message.from_user.id):
        await message.answer(t(user.language, "admin.access_denied"))
        return
    await _edit_or_send(message, t(user.language, "admin.panel_title"), admin_panel_keyboard(user.language))


@router.callback_query(F.data == "admin:open")
async def on_admin_open(callback: CallbackQuery, user: User) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer(t(user.language, "admin.access_denied"), show_alert=True)
        return
    await _edit_or_send(callback, t(user.language, "admin.panel_title"), admin_panel_keyboard(user.language))
    await callback.answer()


def _require_admin(callback: CallbackQuery) -> bool:
    return is_admin(callback.from_user.id)


@router.callback_query(F.data == "admin:overview")
async def on_admin_overview(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    if not _require_admin(callback):
        await callback.answer(t(user.language, "admin.access_denied"), show_alert=True)
        return

    repo = StatsRepository(session)
    total_users = await repo.total_users()
    completed = await repo.total_completed_tests()
    activity = await repo.activity_window()
    completion_rate = round(completed / total_users * 100, 1) if total_users else 0.0
    avg_tests = round(completed / total_users, 2) if total_users else 0.0

    lang = user.language
    lines = [
        t(lang, "admin.overview_title"),
        "",
        t(lang, "admin.overview_users", users=total_users),
        t(lang, "admin.overview_completed", completed=completed),
        t(lang, "admin.overview_completion_rate", rate=completion_rate),
        t(lang, "admin.overview_avg", avg=avg_tests),
        "",
        t(lang, "admin.overview_today", today=activity["today"]["new_users"]),
        t(lang, "admin.overview_week", week=activity["last_7_days"]["new_users"]),
        t(lang, "admin.overview_month", month=activity["last_30_days"]["new_users"]),
    ]
    await _edit_or_send(callback, "\n".join(lines), admin_panel_keyboard(lang))
    await callback.answer()


@router.callback_query(F.data == "admin:distribution")
async def on_admin_distribution(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    if not _require_admin(callback):
        await callback.answer(t(user.language, "admin.access_denied"), show_alert=True)
        return

    repo = StatsRepository(session)
    distribution = await repo.mbti_type_distribution()
    total = sum(distribution.values())
    lang = user.language

    lines = [t(lang, "admin.btn_distribution"), ""]
    if not distribution:
        lines.append(t(lang, "stats.not_available"))
    else:
        ordered = sorted(distribution.items(), key=lambda kv: kv[1], reverse=True)
        for mbti_type, count in ordered:
            pct = round(count / total * 100, 1) if total else 0.0
            bar_len = round(count / ordered[0][1] * 10) if ordered[0][1] else 0
            lines.append(f"{mbti_type} {'█' * bar_len} {count} — {pct}%")
        lines.append("")
        most_common = ordered[0]
        least_common = ordered[-1]
        lines.append(t(lang, "admin.distribution_most_common", type=most_common[0], count=most_common[1]))
        lines.append(t(lang, "admin.distribution_least_common", type=least_common[0], count=least_common[1]))

    await _edit_or_send(callback, "\n".join(lines), admin_panel_keyboard(lang))
    await callback.answer()


@router.callback_query(F.data == "admin:dimensions")
async def on_admin_dimensions(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    if not _require_admin(callback):
        await callback.answer(t(user.language, "admin.access_denied"), show_alert=True)
        return

    repo = StatsRepository(session)
    letters = await repo.axis_letter_counts()
    lang = user.language

    lines = [t(lang, "admin.dimensions_title"), ""]
    for left, right in (("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")):
        total = letters[left] + letters[right]
        left_pct = round(letters[left] / total * 100, 1) if total else 0.0
        right_pct = round(letters[right] / total * 100, 1) if total else 0.0
        lines.append(f"{left}/{right}")
        lines.append(f"{left} {left_pct}%   {right} {right_pct}%")
        lines.append("")

    await _edit_or_send(callback, "\n".join(lines), admin_panel_keyboard(lang))
    await callback.answer()


@router.callback_query(F.data == "admin:languages")
async def on_admin_languages(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    if not _require_admin(callback):
        await callback.answer(t(user.language, "admin.access_denied"), show_alert=True)
        return

    repo = StatsRepository(session)
    breakdown = await repo.language_breakdown()
    lang = user.language

    lines = [t(lang, "admin.languages_title"), ""]
    labels = {"en": "🇬🇧 English", "ru": "🇷🇺 Russian", "unset": "❔ Unset"}
    for code, stats in breakdown.items():
        label = labels.get(code, code)
        lines.append(f"{label}: {stats['users']} users, {stats['completed']} completed")

    await _edit_or_send(callback, "\n".join(lines), admin_panel_keyboard(lang))
    await callback.answer()


@router.callback_query(F.data == "admin:export")
async def on_admin_export(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    if not _require_admin(callback):
        await callback.answer(t(user.language, "admin.access_denied"), show_alert=True)
        return

    lang = user.language
    await callback.answer(t(lang, "admin.export_generating"))

    repo = StatsRepository(session)
    rows = await repo.export_rows()

    buffer = io.StringIO()
    fieldnames = [
        "telegram_id", "language", "mbti_type",
        "e_score", "i_score", "s_score", "n_score",
        "t_score", "f_score", "j_score", "p_score",
        "created_at",
    ]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

    filename = f"mindtype_export_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv"
    document = BufferedInputFile(buffer.getvalue().encode("utf-8"), filename=filename)

    if callback.message is not None:
        await callback.message.answer_document(
            document, caption=t(lang, "admin.export_caption", count=len(rows))
        )

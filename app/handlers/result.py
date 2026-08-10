from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.type_descriptions import TYPE_DESCRIPTIONS
from app.database.models import TestResult, User
from app.database.repositories.result_repo import ResultRepository
from app.database.repositories.stats_repo import StatsRepository
from app.keyboards.test import result_actions_keyboard
from app.keyboards.user import back_to_menu_keyboard
from app.services import statistics_service
from app.services.localization import t
from app.services.mbti_engine import AXES, MBTI_TITLES

router = Router(name="result")


def _bar(percent: float, length: int = 10) -> str:
    filled = round(percent / 100 * length)
    filled = max(0, min(length, filled))
    return "█" * filled + "░" * (length - filled)


def format_result_text(result: TestResult, language: str) -> str:
    title = MBTI_TITLES.get(result.mbti_type, {}).get(language, "")
    lines = [
        t(language, "result.title"),
        "",
        f"*{result.mbti_type}*",
        f"{title}" if title else "",
        "",
        t(language, "result.balance_title"),
    ]

    scores = {
        "E": result.e_score, "I": result.i_score,
        "S": result.s_score, "N": result.n_score,
        "T": result.t_score, "F": result.f_score,
        "J": result.j_score, "P": result.p_score,
    }
    for axis_index, (left, right) in enumerate(AXES):
        winner_letter = result.mbti_type[axis_index]
        left_score, right_score = scores[left], scores[right]
        total = left_score + right_score
        winner_score = scores[winner_letter]
        pct = round(winner_score / total * 100) if total else 50
        lines.append(f"{winner_letter} {_bar(pct)} {pct}%")

    lines.append("")
    description = TYPE_DESCRIPTIONS.get(result.mbti_type, {})
    section_map = [
        ("personality", "result.section_personality"),
        ("strengths", "result.section_strengths"),
        ("challenges", "result.section_challenges"),
        ("work_style", "result.section_work_style"),
        ("communication_style", "result.section_communication"),
    ]
    for field_name, label_key in section_map:
        text = description.get(field_name, {}).get(language)
        if text:
            lines.append(f"{t(language, label_key)}: {text}")

    lines.append("")
    lines.append(f"_{t(language, 'result.disclaimer')}_")

    return "\n".join(line for line in lines if line is not None)


async def render_result(
    target: Message | CallbackQuery, user: User, session: AsyncSession, result: TestResult
) -> None:
    text = format_result_text(result, user.language)
    keyboard = result_actions_keyboard(user.language, result.mbti_type)

    count, total, percent = await statistics_service.get_bot_stat_for_type(StatsRepository(session), result.mbti_type)
    comparison_lines = [
        "",
        t(user.language, "result.bot_comparison_title"),
        f"{t(user.language, 'result.your_type')} {result.mbti_type}",
        t(user.language, "result.bot_users_share", count=count, total=total, percent=percent),
    ]
    text = text + "\n" + "\n".join(comparison_lines)

    if isinstance(target, CallbackQuery):
        if target.message is not None:
            try:
                await target.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
            except Exception:
                await target.message.answer(text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await target.answer(text, reply_markup=keyboard, parse_mode="Markdown")


@router.callback_query(F.data == "menu:result")
async def on_my_result(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    result = await ResultRepository(session).get_latest_for_user(user.id)
    if result is None:
        if callback.message is not None:
            await callback.message.edit_text(
                t(user.language, "result.no_result"), reply_markup=back_to_menu_keyboard(user.language)
            )
        await callback.answer()
        return

    await render_result(callback, user, session, result)
    await callback.answer()


@router.callback_query(F.data.startswith("share:"))
async def on_share(callback: CallbackQuery, user: User) -> None:
    mbti_type = callback.data.split(":", 1)[1]
    share_text = t(user.language, "result.share_text", type=mbti_type)
    await callback.answer()
    if callback.message is not None:
        await callback.message.answer(share_text)

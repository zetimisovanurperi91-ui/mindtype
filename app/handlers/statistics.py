from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.database.repositories.stats_repo import StatsRepository
from app.keyboards.statistics import statistics_menu_keyboard
from app.keyboards.user import back_to_menu_keyboard
from app.services import statistics_service
from app.services.localization import t

router = Router(name="statistics")

AXIS_TITLE_KEYS = {"EI": "stats.menu_ei", "SN": "stats.menu_sn", "TF": "stats.menu_tf", "JP": "stats.menu_jp"}


async def _edit(callback: CallbackQuery, text: str, keyboard) -> None:
    if callback.message is not None:
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except Exception:
            await callback.message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == "menu:stats")
async def on_stats_menu(callback: CallbackQuery, user: User) -> None:
    await _edit(callback, t(user.language, "stats.menu_title"), statistics_menu_keyboard(user.language))
    await callback.answer()


@router.callback_query(F.data.startswith("stats:axis:"))
async def on_axis_stat(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    axis = callback.data.split(":")[2]
    lang = user.language

    research = statistics_service.get_research_stat_for_axis(axis, lang)
    bot_stat = await statistics_service.get_bot_axis_stat(StatsRepository(session), axis)

    title = t(lang, AXIS_TITLE_KEYS.get(axis, "stats.menu_ei"))
    lines = [title, ""]

    lines.append(t(lang, "stats.research_header"))
    if research.available:
        lines.append(research.value_text or "")
        lines.append(t(lang, "stats.source", source=research.source))
        lines.append(t(lang, "stats.year", year=research.year))
        lines.append(t(lang, "stats.population", population=research.population))
        if research.caveat:
            lines.append(f"\n{t(lang, 'stats.caveat_title')}: {research.caveat}")
    else:
        lines.append(t(lang, "stats.not_available"))

    lines.append("")
    lines.append(t(lang, "stats.bot_header"))
    lines.append(t(lang, "stats.among_bot_users", total=bot_stat.total_completed))
    for letter, (count, pct) in bot_stat.breakdown.items():
        lines.append(f"{letter}: {count} ({pct}%)")

    await _edit(callback, "\n".join(lines), statistics_menu_keyboard(lang))
    await callback.answer()


@router.callback_query(F.data == "stats:types")
async def on_type_stats_menu(callback: CallbackQuery, session: AsyncSession, user: User) -> None:
    lang = user.language
    bot_stat = await statistics_service.get_bot_type_distribution(StatsRepository(session))

    lines = [t(lang, "stats.menu_types"), "", t(lang, "stats.research_header")]
    lines.append(
        "INTJ ~2.1%, INFJ ~1.5%, ISFJ ~13.8%, ESFJ ~12.3%, ISTJ ~11.6%, ISFP ~8.8%, "
        "ESTJ ~8.7%, ESFP ~8.5%, ENFP ~8.1%, ISTP ~5.4%, INFP ~4.3%, ESTP ~4.3%, "
        "INTP ~3.3%, ENTP ~3.2%, ENFJ ~2.4%, ENTJ ~1.8%"
    )
    lines.append(t(lang, "stats.source", source="Myers & Briggs Foundation - estimated type frequencies"))
    lines.append(t(lang, "stats.year", year="1972-2002"))
    lines.append(
        t(
            lang,
            "stats.population",
            population="US-based MBTI takers (CAPT / The Myers-Briggs Company / SRI data banks), self-selected.",
        )
    )

    lines.append("")
    lines.append(t(lang, "stats.bot_header"))
    lines.append(t(lang, "stats.among_bot_users", total=bot_stat.total_completed))
    for mbti_type, (count, pct) in list(bot_stat.breakdown.items())[:16]:
        lines.append(f"{mbti_type}: {count} ({pct}%)")

    await _edit(callback, "\n".join(lines), statistics_menu_keyboard(lang))
    await callback.answer()

from __future__ import annotations

from dataclasses import dataclass

from app.data.sources import (
    AXIS_CAVEAT,
    AXIS_FREQUENCIES,
    MBTI_TYPE_FREQUENCIES,
    NOT_AVAILABLE_TEXT,
    SOURCE_LABEL,
    SOURCE_POPULATION,
    SOURCE_URL,
    SOURCE_YEARS,
)
from app.database.repositories.stats_repo import StatsRepository


@dataclass
class ResearchStat:
    """A citeable, published figure. Never derived from this bot's own users."""

    available: bool
    value_text: str | None = None
    source: str | None = None
    year: str | None = None
    population: str | None = None
    url: str | None = None
    caveat: str | None = None


@dataclass
class BotStat:
    """A figure computed live from this bot's own database. Never presented
    as if it describes the world population."""

    total_completed: int
    breakdown: dict[str, tuple[int, float]]  # label -> (count, percent)


def get_research_stat_for_type(mbti_type: str, language: str) -> ResearchStat:
    value = MBTI_TYPE_FREQUENCIES.get(mbti_type.upper())
    if value is None:
        return ResearchStat(available=False)
    return ResearchStat(
        available=True,
        value_text=f"~{value}%",
        source=SOURCE_LABEL,
        year=SOURCE_YEARS,
        population=SOURCE_POPULATION,
        url=SOURCE_URL,
    )


def get_research_stat_for_axis(axis: str, language: str) -> ResearchStat:
    """axis: 'EI', 'SN', 'TF', or 'JP'"""
    frequencies = AXIS_FREQUENCIES.get(axis)
    if frequencies is None:
        return ResearchStat(available=False)
    parts = ", ".join(f"{letter} {pct}%" for letter, pct in frequencies.items())
    return ResearchStat(
        available=True,
        value_text=parts,
        source=SOURCE_LABEL,
        year=SOURCE_YEARS,
        population=SOURCE_POPULATION,
        url=SOURCE_URL,
        caveat=AXIS_CAVEAT.get(language, AXIS_CAVEAT["en"]),
    )


def not_available_text(language: str) -> str:
    return NOT_AVAILABLE_TEXT.get(language, NOT_AVAILABLE_TEXT["en"])


async def get_bot_type_distribution(repo: StatsRepository) -> BotStat:
    distribution = await repo.mbti_type_distribution()
    total = sum(distribution.values())
    breakdown = {}
    for mbti_type, count in sorted(distribution.items(), key=lambda kv: kv[1], reverse=True):
        pct = round(count / total * 100, 1) if total else 0.0
        breakdown[mbti_type] = (count, pct)
    return BotStat(total_completed=total, breakdown=breakdown)


async def get_bot_axis_stat(repo: StatsRepository, axis: str) -> BotStat:
    letters = await repo.axis_letter_counts()
    left, right = axis[0], axis[1]
    total = letters[left] + letters[right]
    breakdown = {}
    for letter in (left, right):
        pct = round(letters[letter] / total * 100, 1) if total else 0.0
        breakdown[letter] = (letters[letter], pct)
    return BotStat(total_completed=total, breakdown=breakdown)


async def get_bot_stat_for_type(repo: StatsRepository, mbti_type: str) -> tuple[int, int, float]:
    """Returns (count_for_type, total_completed, percent) for the personal
    'how common is my type among MindType users' comparison on the result page."""
    distribution = await repo.mbti_type_distribution()
    total = sum(distribution.values())
    count = distribution.get(mbti_type.upper(), 0)
    percent = round(count / total * 100, 1) if total else 0.0
    return count, total, percent

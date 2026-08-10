"""
Pure scoring logic for the MBTI test.

This module has zero dependencies on Telegram or the database - it takes
plain data in and returns plain data out, so it can be unit tested with
simple dicts (see tests/test_mbti_engine.py).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.data.questions import QUESTIONS, get_question

AXES: list[tuple[str, str]] = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]

# Deterministic fallback order used only if BOTH poles of an axis end up with
# an identical score (a true tie). This never overrides a real signal - it
# only breaks a 0-0 or exact-equal situation so the type is always defined.
_TIE_BREAK_DEFAULT = {"E": False, "S": False, "T": True, "J": True}
# False -> default to the "left" letter of the pair name (E, S, T, J) is not
# always what we want, so we spell it out explicitly below instead.
_TIE_BREAK_LETTER = {"EI": "I", "SN": "N", "TF": "T", "JP": "J"}


@dataclass
class AxisResult:
    letter: str
    opposite_letter: str
    score: int
    opposite_score: int
    confidence: float  # 0-100, "how much this axis's answers leaned one way"

    @property
    def as_bar(self) -> tuple[str, int]:
        """Returns (winning_letter, confidence_percent) for rendering a bar."""
        return self.letter, round(self.confidence)


@dataclass
class MBTIResult:
    mbti_type: str
    raw_scores: dict[str, int] = field(default_factory=dict)
    axes: dict[str, AxisResult] = field(default_factory=dict)  # keyed by "EI", "SN", ...


def score_answers(answers: dict[int, dict[str, int]]) -> MBTIResult:
    """
    answers: mapping of question_id -> the weight dict of the option the
             user picked, e.g. {1: {"E": 2}, 2: {"I": 2}, ...}

    Returns an MBTIResult with the final 4-letter type and per-axis
    confidence. Confidence is explicitly a "test score balance" figure,
    not a claim of psychological certainty - that framing lives in the
    locale strings that render this result.
    """
    raw_scores: dict[str, int] = {letter: 0 for pair in AXES for letter in pair}

    for question_id, weights in answers.items():
        question = get_question(question_id)
        if question is None:
            # Defensive: ignore answers for unknown/stale question ids
            # rather than crashing a user's session.
            continue
        for letter, points in weights.items():
            if letter in raw_scores:
                raw_scores[letter] += points

    mbti_letters: list[str] = []
    axes_result: dict[str, AxisResult] = {}

    for left, right in AXES:
        axis_key = f"{left}{right}"
        left_score = raw_scores[left]
        right_score = raw_scores[right]
        total = left_score + right_score

        if total == 0:
            # No answers registered for this axis at all (shouldn't happen
            # in normal flow, but guard against partial/corrupted sessions).
            winner = _TIE_BREAK_LETTER[axis_key]
            confidence = 50.0
        elif left_score == right_score:
            winner = _TIE_BREAK_LETTER[axis_key]
            confidence = 50.0
        else:
            winner = left if left_score > right_score else right
            confidence = max(left_score, right_score) / total * 100

        loser = right if winner == left else left
        winner_score = raw_scores[winner]
        loser_score = raw_scores[loser]

        mbti_letters.append(winner)
        axes_result[axis_key] = AxisResult(
            letter=winner,
            opposite_letter=loser,
            score=winner_score,
            opposite_score=loser_score,
            confidence=confidence,
        )

    return MBTIResult(
        mbti_type="".join(mbti_letters),
        raw_scores=raw_scores,
        axes=axes_result,
    )


def total_questions() -> int:
    return len(QUESTIONS)


MBTI_TITLES: dict[str, dict[str, str]] = {
    "INTJ": {"en": "The Architect", "ru": "Архитектор"},
    "INTP": {"en": "The Logician", "ru": "Логик"},
    "ENTJ": {"en": "The Commander", "ru": "Командир"},
    "ENTP": {"en": "The Debater", "ru": "Полемист"},
    "INFJ": {"en": "The Advocate", "ru": "Активист"},
    "INFP": {"en": "The Mediator", "ru": "Посредник"},
    "ENFJ": {"en": "The Protagonist", "ru": "Тренер"},
    "ENFP": {"en": "The Campaigner", "ru": "Борец"},
    "ISTJ": {"en": "The Logistician", "ru": "Администратор"},
    "ISFJ": {"en": "The Defender", "ru": "Защитник"},
    "ESTJ": {"en": "The Executive", "ru": "Управляющий"},
    "ESFJ": {"en": "The Consul", "ru": "Консул"},
    "ISTP": {"en": "The Virtuoso", "ru": "Виртуоз"},
    "ISFP": {"en": "The Adventurer", "ru": "Артист"},
    "ESTP": {"en": "The Entrepreneur", "ru": "Делец"},
    "ESFP": {"en": "The Entertainer", "ru": "Развлекатель"},
}

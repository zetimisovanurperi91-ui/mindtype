"""
Curated, citeable research statistics used to seed the `statistic_sources`
table (see database/models.py::StatisticSource).

IMPORTANT: every number here traces back to a real, checkable source. These
are widely-cited "estimated frequency" figures published by the Myers &
Briggs Foundation, compiled from MBTI data banks collected 1972-2002 in the
United States (CAPT, The Myers-Briggs Company, and SRI data pools). They are
NOT a random or representative sample of the world's population - they come
from people who took the MBTI, disproportionately in US professional,
educational, and counseling contexts. The bot always shows this context
alongside the numbers and never states them as "world population" figures.

If you don't have a similarly checkable citation for something, don't add
it here - the statistics screen is written to show "reliable data not
available" rather than a placeholder number.
"""

from __future__ import annotations

SOURCE_LABEL = "Myers & Briggs Foundation - estimated type frequencies"
SOURCE_YEARS = "1972-2002 (data compiled through 2002)"
SOURCE_POPULATION = (
    "US-based individuals who took the MBTI instrument, pooled from CAPT, "
    "The Myers-Briggs Company, and SRI data banks. Self-selected, not a "
    "random sample of the general population."
)
SOURCE_URL = "https://www.myersbriggs.org/my-mbti-personality-type/my-mbti-results/how-frequent-is-my-type/"

# category -> {"en": text, "ru": text} percentage figures (rounded to 1 decimal)
MBTI_TYPE_FREQUENCIES: dict[str, float] = {
    "ISFJ": 13.8, "ESFJ": 12.3, "ISTJ": 11.6, "ISFP": 8.8,
    "ESTJ": 8.7, "ESFP": 8.5, "ENFP": 8.1, "ISTP": 5.4,
    "INFP": 4.3, "ESTP": 4.3, "INTP": 3.3, "ENTP": 3.2,
    "ENFJ": 2.4, "INTJ": 2.1, "ENTJ": 1.8, "INFJ": 1.5,
}

# Axis splits, same source family, presented with the same caveats.
AXIS_FREQUENCIES: dict[str, dict[str, float]] = {
    "EI": {"E": 49.3, "I": 50.7},
    "SN": {"S": 73.3, "N": 26.7},
    "TF": {"T": 40.2, "F": 59.8},
    "JP": {"J": 54.1, "P": 45.9},
}

AXIS_CAVEAT = {
    "en": (
        "This reflects one widely-cited US-based data pool, not a scientific "
        "census of humanity. Distributions shift noticeably by country, "
        "culture, and how the sample was collected."
    ),
    "ru": (
        "Это отражает один часто цитируемый набор данных из США, а не "
        "научную перепись человечества. Распределение заметно меняется в "
        "зависимости от страны, культуры и способа сбора выборки."
    ),
}

NOT_AVAILABLE_TEXT = {
    "en": "Reliable worldwide data for this exact statistic is not available.",
    "ru": "Достоверных общемировых данных по этому показателю не существует.",
}

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_LOCALES_DIR = Path(__file__).resolve().parent.parent / "locales"
_SUPPORTED_LANGUAGES = ("en", "ru")
_DEFAULT_LANGUAGE = "en"

_cache: dict[str, dict[str, str]] = {}


def _load(language: str) -> dict[str, str]:
    if language not in _cache:
        path = _LOCALES_DIR / f"{language}.json"
        with path.open("r", encoding="utf-8") as f:
            _cache[language] = json.load(f)
    return _cache[language]


def normalize_language(language: str | None) -> str:
    if language in _SUPPORTED_LANGUAGES:
        return language  # type: ignore[return-value]
    return _DEFAULT_LANGUAGE


def t(language: str | None, key: str, **kwargs: Any) -> str:
    """Translate `key` into `language`, formatting any {placeholders}.
    Falls back to English, then to the raw key, so a missing translation
    never crashes a handler."""
    lang = normalize_language(language)
    strings = _load(lang)
    text = strings.get(key)
    if text is None:
        text = _load(_DEFAULT_LANGUAGE).get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text


def preload_all() -> None:
    for lang in _SUPPORTED_LANGUAGES:
        _load(lang)

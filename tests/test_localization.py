from app.services.localization import normalize_language, t


def test_normalize_language_supported():
    assert normalize_language("en") == "en"
    assert normalize_language("ru") == "ru"


def test_normalize_language_falls_back_to_english():
    assert normalize_language(None) == "en"
    assert normalize_language("fr") == "en"
    assert normalize_language("") == "en"


def test_translation_returns_localized_string():
    en_text = t("en", "menu.take_test")
    ru_text = t("ru", "menu.take_test")
    assert en_text != ru_text
    assert "test" in en_text.lower()


def test_translation_formats_placeholders():
    text = t("en", "test.question_progress", current=3, total=15)
    assert "3" in text
    assert "15" in text


def test_translation_falls_back_to_key_if_missing_everywhere():
    text = t("en", "this.key.does.not.exist")
    assert text == "this.key.does.not.exist"


def test_translation_unsupported_language_falls_back_to_english():
    text = t("de", "menu.take_test")
    assert text == t("en", "menu.take_test")

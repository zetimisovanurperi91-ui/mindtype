from app.config import settings
from app.services.admin_service import is_admin


def test_is_admin_true_for_configured_id(monkeypatch):
    monkeypatch.setattr(settings, "admin_ids", "111,222")
    assert is_admin(111) is True
    assert is_admin(222) is True


def test_is_admin_false_for_unknown_id(monkeypatch):
    monkeypatch.setattr(settings, "admin_ids", "111,222")
    assert is_admin(333) is False


def test_is_admin_false_when_no_admins_configured(monkeypatch):
    monkeypatch.setattr(settings, "admin_ids", "")
    assert is_admin(111) is False


def test_admin_ids_parsing_handles_whitespace(monkeypatch):
    monkeypatch.setattr(settings, "admin_ids", " 111 , 222 ,,333")
    assert settings.admin_id_set == frozenset({111, 222, 333})

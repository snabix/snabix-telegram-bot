from pytest import MonkeyPatch

from snabix_bot.config import Settings


def test_settings_parses_admin_ids(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("SNABIX_BOT_TOKEN", "token")
    monkeypatch.setenv("SNABIX_BACKEND_BASE_URL", "http://backend.test/api/v1")
    monkeypatch.setenv("SNABIX_BACKEND_SERVICE_TOKEN", "service-token")
    monkeypatch.setenv("SNABIX_ADMIN_TELEGRAM_IDS", "1, 2,3")

    settings = Settings(**{})

    assert settings.admin_ids == frozenset({1, 2, 3})

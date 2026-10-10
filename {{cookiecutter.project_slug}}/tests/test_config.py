from __future__ import annotations

import pytest

from src.core.config import Settings, parse_admin_ids


def test_parse_admin_ids_from_string() -> None:
    assert parse_admin_ids("1, 2 ,3") == [1, 2, 3]


def test_parse_admin_ids_variants() -> None:
    assert parse_admin_ids(None) == []
    assert parse_admin_ids(7) == [7]
    assert parse_admin_ids([1, 2]) == [1, 2]


def test_parse_admin_ids_ignores_invalid_tokens() -> None:
    assert parse_admin_ids("1,not-a-number,3") == [1, 3]


def test_settings_reads_token_and_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:abc")
    settings = Settings(_env_file=None)
    assert settings.bot_token == "123:abc"
    assert settings.admin_ids == []
    assert settings.metrics_port == {{ cookiecutter.port }}


def test_settings_requires_bot_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    with pytest.raises(RuntimeError):
        Settings(_env_file=None)

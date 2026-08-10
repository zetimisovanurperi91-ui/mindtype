from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str
    database_url: str
    admin_ids: str = ""  # comma-separated telegram user ids, e.g. "123,456"

    @property
    def admin_id_set(self) -> frozenset[int]:
        ids: set[int] = set()
        for chunk in self.admin_ids.split(","):
            chunk = chunk.strip()
            if chunk:
                ids.add(int(chunk))
        return frozenset(ids)


settings = Settings()  # type: ignore[call-arg]  # values come from .env / real env vars

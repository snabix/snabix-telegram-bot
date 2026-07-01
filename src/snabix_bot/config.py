from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SNABIX_",
        extra="ignore",
    )

    bot_token: str = Field(alias="SNABIX_BOT_TOKEN")
    bot_mode: Literal["polling", "webhook"] = Field(default="polling", alias="SNABIX_BOT_MODE")
    backend_base_url: str = Field(alias="SNABIX_BACKEND_BASE_URL")
    backend_service_token: str = Field(alias="SNABIX_BACKEND_SERVICE_TOKEN")
    admin_panel_url: str = Field(
        default="http://127.0.0.1:8080/admin",
        alias="SNABIX_ADMIN_PANEL_URL",
    )
    admin_telegram_ids: str = Field(
        default="",
        alias="SNABIX_ADMIN_TELEGRAM_IDS",
    )
    webhook_url: str = Field(default="", alias="SNABIX_BOT_WEBHOOK_URL")
    webhook_path: str = Field(default="/webhook/telegram", alias="SNABIX_BOT_WEBHOOK_PATH")
    webhook_secret: str = Field(default="", alias="SNABIX_BOT_WEBHOOK_SECRET")
    webhook_host: str = Field(default="0.0.0.0", alias="SNABIX_BOT_HOST")
    webhook_port: int = Field(default=9000, alias="SNABIX_BOT_PORT")
    log_level: str = Field(default="INFO", alias="SNABIX_LOG_LEVEL")

    @property
    def admin_ids(self) -> frozenset[int]:
        return frozenset(
            int(part.strip()) for part in self.admin_telegram_ids.split(",") if part.strip()
        )

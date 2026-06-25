from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SNABIX_",
        extra="ignore",
    )

    bot_token: str = Field(alias="SNABIX_BOT_TOKEN")
    backend_base_url: str = Field(alias="SNABIX_BACKEND_BASE_URL")
    backend_service_token: str = Field(alias="SNABIX_BACKEND_SERVICE_TOKEN")
    admin_telegram_ids: str = Field(
        default="",
        alias="SNABIX_ADMIN_TELEGRAM_IDS",
    )
    log_level: str = Field(default="INFO", alias="SNABIX_LOG_LEVEL")

    @property
    def admin_ids(self) -> frozenset[int]:
        return frozenset(
            int(part.strip())
            for part in self.admin_telegram_ids.split(",")
            if part.strip()
        )

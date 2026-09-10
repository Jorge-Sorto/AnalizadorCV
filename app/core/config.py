from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Analizador inteligente de CV"
    app_version: str = "1.0.0"
    app_env: str = "development"
    llm_provider: str = "demo"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5-mini"
    llm_timeout_seconds: float = Field(default=30, gt=0, le=120)
    cors_origins: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

    @property
    def model_ready(self) -> bool:
        return self.llm_provider == "demo" or bool(self.openai_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()

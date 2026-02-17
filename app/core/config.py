
from typing import Literal
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "Invoice Matcher Agent"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    LLM_API_KEY: SecretStr
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    EMAIL_USER: str | None = None
    EMAIL_PASSWORD: SecretStr | None = None
    GEMINI_API_KEY: SecretStr | None = None



settings = Settings()

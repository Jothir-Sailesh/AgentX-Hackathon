from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    # Core
    PROJECT_NAME: str = "AgentX MVP"
    SECRET_KEY: SecretStr
    LLM_API_KEY: SecretStr

    # Gmail / IMAP
    GMAIL_EMAIL: str
    GMAIL_APP_PASSWORD: SecretStr
    IMAP_SERVER: str = "imap.gmail.com"
    IMAP_PORT: int = 993

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

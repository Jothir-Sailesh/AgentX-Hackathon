from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Invoice Matcher Agent"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "change_me_in_production"
    
    # External Services
    LLM_API_KEY: str = ""

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

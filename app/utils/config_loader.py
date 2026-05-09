from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Centralized application settings.
    Automatically loads values from .env
    """

    APP_NAME: str = "CloudDash Multi-Agent Support System"
    APP_VERSION: str = "1.0.0"

    GROQ_API_KEY: str = Field(...)

    LANGCHAIN_API_KEY: str | None = None
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_PROJECT: str = "CloudDash-MultiAgent-System"

    LOG_LEVEL: str = "INFO"

    HF_TOKEN: str | None = None

    VECTOR_DB_DIR: str = "./chroma_db"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
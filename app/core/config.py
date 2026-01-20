from typing import Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool = False

    SCRAPE_SCHEDULE_TIME: str = "12:00"
    TIMEZONE: str = "GMT"

    TARGET_URL: str
    MAX_CRAWL_DEPTH: int = 3
    MAX_WORKERS: int = 5
    RETRY_ATTEMPTS: int = 3

    HTML_STORAGE_PATH: str = "./storage/html"
    MARKDOWN_STORAGE_PATH: str = "./storage/markdown"
    TASKS_STORAGE_PATH: str = "./storage/tasks"

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/scraper.log"

    GOOGLE_API_KEY: str
    DB_NAME: str = "database"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "webscraper"

    DB_URL: Optional[str] = None

    @model_validator(mode="after")
    def assemble_db_connection(self) -> "Settings":
        if not self.DB_URL:
            self.DB_URL = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        return self

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )


settings = Settings()

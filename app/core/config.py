import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool = False

    # Scheduling
    SCRAPE_SCHEDULE_TIME: str = "12:00"
    TIMEZONE: str = "UTC"

    # Scraping
    TARGET_URL: str
    MAX_CRAWL_DEPTH: int = 3
    REQUEST_TIMEOUT: int = 30
    MAX_CONCURRENT_REQUESTS: int = 10
    RETRY_ATTEMPTS: int = 3

    # Storage
    HTML_STORAGE_PATH: str = "./storage/html"
    MARKDOWN_STORAGE_PATH: str = "./storage/markdown"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/scraper.log"

    # Pydantic configuration to read from .env
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )


# Create a global instance of settings
settings = Settings()

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

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/scraper.log"

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )


settings = Settings()

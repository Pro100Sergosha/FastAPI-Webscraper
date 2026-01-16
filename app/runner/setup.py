import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.scheduler import setup_scheduler, shutdown_scheduler
from app.routers import scraper

logger = logging.getLogger(__name__)


def ensure_storage_directories():
    required_paths = [
        settings.HTML_STORAGE_PATH,
        settings.MARKDOWN_STORAGE_PATH,
        settings.TASKS_STORAGE_PATH,
    ]

    for path in required_paths:
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
                logger.info(f"Created missing storage directory: {path}")
            except Exception as e:
                logger.error(f"Failed to create directory {path}: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up..")
    ensure_storage_directories()
    setup_scheduler()
    yield
    shutdown_scheduler()
    logger.info("Application shutting down..")


def setup() -> FastAPI:
    setup_logging()
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
    )
    app.include_router(scraper.router)
    return app

from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
import logging

# Setup logging on startup
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Scraper API is running",
        "config": {
            "target": settings.TARGET_URL,
            "mode": "Debug" if settings.DEBUG else "Production",
        },
    }

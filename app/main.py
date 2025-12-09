import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.scheduler import setup_scheduler, shutdown_scheduler

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up..")
    setup_scheduler()
    yield
    shutdown_scheduler()
    logger.info("Application shutting down..")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


app.include_router(api_router, prefix="/api/v1")

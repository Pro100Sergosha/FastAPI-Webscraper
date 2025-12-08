import logging
import uuid
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.config import settings
from app.services.crawler import CrawlerService
from app.services.job_store import JobStore
from app.services.parser import HtmlToMarkdownParser
from app.services.storage import FileSystemStorage

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def run_scheduled_scrape():
    logger.info("Starting scheduled scraping job...")

    task_id = f"auto_{uuid.uuid4()}"

    html_storage = FileSystemStorage(settings.HTML_STORAGE_PATH)
    md_storage = FileSystemStorage(settings.MARKDOWN_STORAGE_PATH)
    job_store = JobStore()
    parser = HtmlToMarkdownParser()

    crawler = CrawlerService(
        storage=html_storage, md_storage=md_storage, job_store=job_store, parser=parser
    )

    max_depth = settings.MAX_CRAWL_DEPTH
    target_url = settings.TARGET_URL

    est_minutes = 5 * max_depth
    now = datetime.now(timezone.utc)
    estimated_completion = now + timedelta(minutes=est_minutes)

    await job_store.create_job(
        task_id,
        {
            "task_id": task_id,
            "url": target_url,
            "status": "queued",
            "type": "scheduled",
            "downloaded_files": 0,
            "total_links_found": 0,
            "internal_estimated_completion": estimated_completion.isoformat(),
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        },
    )

    try:
        await crawler.start(start_url=target_url, task_id=task_id, max_depth=max_depth)
        logger.info(f"Scheduled job {task_id} finished successfully.")
    except Exception as e:
        logger.error(f"Scheduled job {task_id} failed: {e}")


def setup_scheduler():
    hour, minute = map(int, settings.SCRAPE_SCHEDULE_TIME.split(":"))

    trigger = CronTrigger(hour=hour, minute=minute, timezone=settings.TIMEZONE)

    scheduler.add_job(
        run_scheduled_scrape, trigger=trigger, id="daily_scrape", replace_existing=True
    )

    logger.info(
        f"Scheduler set up. Job will run daily at {settings.SCRAPE_SCHEDULE_TIME} ({settings.TIMEZONE})"
    )

    scheduler.start()


def shutdown_scheduler():
    scheduler.shutdown()

import os
import uuid

import aiofiles
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from app.api.deps import get_crawler_service, get_job_store
from app.core.config import settings
from app.models.models import (
    LogResponse,
    StatusResponse,
    TriggerRequest,
    TriggerResponse,
)
from app.services.crawler import CrawlerService
from app.services.job_store import JobStore

router = APIRouter()


@router.post("/scraper/trigger", response_model=TriggerResponse)
async def trigger_scraper(
    request: TriggerRequest,
    background_tasks: BackgroundTasks,
    crawler: CrawlerService = Depends(get_crawler_service),
    job_store: JobStore = Depends(get_job_store),
):
    """
    Starts scraping task and instantly returns ID of the task.
    """
    task_id = str(uuid.uuid4())

    await job_store.create_job(
        task_id,
        {
            "task_id": task_id,
            "url": str(request.url),
            "status": "queued",
            "processed_links": 0,
            "total_links_found": 0,
        },
    )
    background_tasks.add_task(crawler.start, request.url, task_id)

    return TriggerResponse(task_id=task_id, status="queued")


@router.get("/scraper/status/{task_id}", response_model=StatusResponse)
async def get_scraper_status(
    task_id: str, job_store: JobStore = Depends(get_job_store)
):
    """Reads JSON task file and returns its status."""
    job_data = await job_store.get_job(task_id)

    if not job_data:
        raise HTTPException(status_code=404, detail="Task not found")

    return StatusResponse(**job_data)


@router.get("/scraper/logs", response_model=LogResponse)
async def get_logs(limit: int = 50):
    log_path = settings.LOG_FILE

    if not os.path.exists(log_path):
        return LogResponse(
            logs=["Log file not found yet."],
        )

    try:
        async with aiofiles.open(
            log_path, mode="r", encoding="utf-8", errors="ignore"
        ) as f:
            lines = await f.readlines()

            last_lines = lines[-limit:]

            cleaned_logs = [line.strip() for line in last_lines if line.strip()]

            return LogResponse(logs=cleaned_logs)

    except Exception as e:
        return LogResponse(logs=[f"Error reading logs: {str(e)}"])

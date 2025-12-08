from typing import Optional

from pydantic import BaseModel


class TriggerRequest(BaseModel):
    url: str


class TriggerResponse(BaseModel):
    task_id: str
    status: str


class StatusRequest(BaseModel):
    task_id: str


class StatusResponse(BaseModel):
    task_id: str
    status: str
    url: str
    processed_links: int = 0
    total_links_found: int = 0
    created_at: str
    updated_at: Optional[str] = None
    completed_at: Optional[str] = None
    estimated_time_remaining: Optional[str] = None
    error: Optional[str] = None


class LogResponse(BaseModel):
    logs: list[str]

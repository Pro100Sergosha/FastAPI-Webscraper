from functools import lru_cache

from fastapi import Depends
from sqlmodel import Session

from app.core.config import settings
from app.db.database import get_session
from app.infra.ai_providers import GeminiClient
from app.interfaces.ai_client import AIClient
from app.services.chat_service import ChatService
from app.services.crawler import CrawlerService
from app.services.job_store import JobStore
from app.services.parser import HtmlToMarkdownParser
from app.services.storage import FileSystemStorage


def get_job_store() -> JobStore:
    return JobStore()


def get_crawler_service() -> CrawlerService:
    storage = FileSystemStorage(base_path=settings.HTML_STORAGE_PATH)
    job_store = get_job_store()
    md_storage = FileSystemStorage(base_path=settings.MARKDOWN_STORAGE_PATH)
    parser = HtmlToMarkdownParser()
    return CrawlerService(
        storage=storage, job_store=job_store, md_storage=md_storage, parser=parser
    )


@lru_cache()
def get_ai_client() -> AIClient:
    """
    Provides a singleton instance of the AI client (GeminiClient).

    :return: An instance of AIClient.
    """
    return GeminiClient(api_key=settings.GOOGLE_API_KEY)


def get_chat_service(
    session: Session = Depends(get_session),
    ai_client: AIClient = Depends(get_ai_client),
) -> ChatService:
    """
    Dependency provider for ChatService.

    :param session: The database session.
    :param ai_client: The AI client instance.
    :return: An instance of ChatService.
    """
    return ChatService(ai_client=ai_client, session=session)

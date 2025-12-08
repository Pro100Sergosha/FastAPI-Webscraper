from app.core.config import settings
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

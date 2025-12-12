import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.services.crawler import CrawlerService
from app.services.storage import FileSystemStorage
from app.services.parser import HtmlToMarkdownParser


class MockTab:
    def __init__(
        self, html_content="<html><a href='https://test.com/page2'>link</a></html>"
    ):
        self.html = html_content
        self.attrs = {}

    async def get_content(self):
        return self.html

    async def sleep(self, seconds):
        pass

    async def select_all(self, selector):
        if selector == "a":
            link_mock = MagicMock()
            link_mock.attrs.get.return_value = "https://test.com/page2"
            return [link_mock]
        return []

    async def close(self):
        pass


class MockBrowser:
    def __init__(self):
        pass

    async def get(self, url, new_tab=True):
        return MockTab()

    def stop(self):
        pass


@pytest.mark.asyncio
async def test_crawler_service_flow(tmp_path, mock_job_store):
    html_storage = FileSystemStorage(str(tmp_path / "html"))
    md_storage = FileSystemStorage(str(tmp_path / "md"))
    parser = HtmlToMarkdownParser()

    crawler = CrawlerService(
        storage=html_storage,
        job_store=mock_job_store,
        parser=parser,
        md_storage=md_storage,
    )

    crawler.MAX_WORKERS = 1
    crawler.MAX_RETRIES = 0

    task_id = "test-crawl-task"
    start_url = "https://test.com"

    await mock_job_store.create_job(
        task_id, {"task_id": task_id, "url": start_url, "status": "queued"}
    )

    with patch("app.services.crawler.uc") as mock_uc:
        mock_browser = MockBrowser()
        mock_uc.start = AsyncMock(return_value=mock_browser)

        await crawler.start(start_url, task_id, max_depth=1)

        mock_uc.start.assert_called_once()

        job = await mock_job_store.get_job(task_id)
        assert job["status"] == "completed"
        assert "total_time" in job

        assert (tmp_path / "html" / "index.html").exists()
        assert (tmp_path / "md" / "index.md").exists()

        md_content = (tmp_path / "md" / "index.md").read_text(encoding="utf-8")
        assert "Source: https://test.com" in md_content

import asyncio
import logging
import time
from datetime import datetime, timedelta
from urllib.parse import urlparse

import nodriver as uc

from app.core.config import settings
from app.services.base import BaseParserService, BaseStorageBackend
from app.services.job_store import JobStore
from app.services.storage import FileSystemStorage

logger = logging.getLogger(__name__)


class CrawlerService:
    def __init__(
        self,
        storage: FileSystemStorage,
        job_store: JobStore,
        parser: BaseParserService,
        md_storage: BaseStorageBackend,
    ):
        self.storage = storage
        self.job_store = job_store
        self.md_storage = md_storage
        self.parser = parser
        self.visited_urls = set()
        self.block_indicators = [
            "Enable JavaScript",
            "Access denied",
            "403 Forbidden",
            "Please enable JavaScript",
            "Checking your browser",
            "Just a moment",
        ]
        self.MAX_WORKERS = settings.MAX_WORKERS
        self.MAX_DEPTH = settings.MAX_CRAWL_DEPTH
        self.MAX_RETRIES = 3

        self.processed_links = 0
        self.start_time = None
        self.browser = None
        self.base_domain = ""
        self.queue = asyncio.Queue()

    async def start(self, start_url: str, task_id: str, max_depth: int = 2):
        """
        Crawler start.
        Crawler will download all HTML files depended on max depth.
        """
        logger.info(f"=== Starting crawling: {task_id} | Max Depth: {max_depth} ===")

        await self.job_store.update_job(
            task_id,
            {
                "status": "running",
                "total_links_found": len(self.visited_urls),
                "processed_links": 0,
            },
        )
        self.visited_urls = set()
        self.processed_links = 0
        self.start_time = time.time()
        self.MAX_DEPTH = max_depth
        self.base_domain = urlparse(start_url).netloc

        self.browser = await uc.start(headless=False)

        try:
            await self.queue.put((start_url, 0))
            self.visited_urls.add(start_url)

            workers = [
                asyncio.create_task(self._worker(task_id))
                for _ in range(self.MAX_WORKERS)
            ]

            await self.queue.join()

            for w in workers:
                w.cancel()

            total_time = str(timedelta(seconds=int(time.time() - self.start_time)))
            await self.job_store.update_job(
                task_id,
                {
                    "status": "completed",
                    "completed_at": datetime.now().isoformat(),
                    "total_links_found": len(self.visited_urls),
                    "total_time": total_time,
                },
            )
            logger.info(f"Task {task_id} completed successfully")
            logger.info(f"=== Parsed {self.processed_links} links in {total_time} ===")

        except Exception as e:
            logger.error(f"Error within main loop: {e}")

        finally:
            try:
                self.browser.stop()
            except Exception as e:
                logger.error(f"Failed stopping browser: {e}")

    async def _worker(self, task_id: str):
        while True:
            try:
                url, depth = await self.queue.get()
            except asyncio.CancelledError:
                break

            try:
                await self._process_url(url, depth, task_id)
            except Exception as e:
                logger.error(f"Worker error: {e}")
            finally:
                self.queue.task_done()

    async def _process_url(self, url, depth, task_id: str):
        for attempt in range(self.MAX_RETRIES + 1):
            tab = None
            try:
                tab = await self.browser.get(url, new_tab=True)

                html = await self._wait_for_page_load(tab)

                if not html or len(html) < 50:
                    if attempt < self.MAX_RETRIES:
                        await asyncio.sleep(1)
                        continue
                    else:
                        logger.warning(f"Skipping empty/blocked: {url}")
                        return

                filename = self.storage.generate_filename(url)
                await self.storage.save(filename, html)

                parsed_data = await self.parser.parse(html)
                markdown_content = parsed_data["content"]
                filename_md = self.storage.generate_filename(url, ".md")

                full_content = (
                    f"# {parsed_data['title']}\n"
                    f"Source: {url}\n\n"
                    f"{markdown_content}"
                )
                await self.md_storage.save(filename_md, full_content)

                self.processed_links += 1
                eta_str = "Calculating"
                if self.processed_links > 0 and self.start_time:
                    elapsed_time = time.time() - self.start_time
                    avg_time_per_link = elapsed_time / self.processed_links

                    remaining_items = len(self.visited_urls) - self.processed_links

                    if remaining_items < 0:
                        remaining_items = 0

                    eta_seconds = int(avg_time_per_link * remaining_items)
                    eta_str = str(timedelta(seconds=eta_seconds))
                await self.job_store.update_job(
                    task_id,
                    {
                        "processed_links": self.processed_links,
                        "total_links_found": len(self.visited_urls),
                        "estimated_time_remaining": eta_str,
                    },
                )
                if depth < self.MAX_DEPTH:
                    await self._extract_and_enqueue_links(tab, depth + 1)

                return

            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                if attempt < self.MAX_RETRIES:
                    await asyncio.sleep(1)
            finally:
                if tab:
                    try:
                        await tab.close()
                    except Exception as e:
                        logger.error(f"Error occurred with closing the tab: {e}")

    async def _extract_and_enqueue_links(self, tab, next_depth):
        try:
            links_elements = await tab.select_all("a")
            count_added = 0

            for link in links_elements:
                try:
                    href = link.attrs.get("href")

                    if (
                        href
                        and self.base_domain in href
                        and href not in self.visited_urls
                        and not href.endswith(
                            (".png", ".jpg", ".jpeg", ".pdf", ".css", ".js", ".zip")
                        )
                    ):
                        self.visited_urls.add(href)
                        await self.queue.put((href, next_depth))
                        count_added += 1
                except Exception as e:
                    logger.error(f"Error extracting links: {e}")
                    continue

            if count_added > 0:
                logger.info(
                    f"  -> Found {count_added} new links. Queue size: {self.queue.qsize()}"
                )

        except Exception as e:
            logger.error(f"Error extracting links: {e}")

    async def _wait_for_page_load(self, tab):
        try:
            await tab.sleep(2)
            html = await tab.get_content()

            attempts = 0
            while (
                any(indicator in html for indicator in self.block_indicators)
                and attempts < 10
            ):
                await tab.sleep(1.5)
                html = await tab.get_content()
                attempts += 1
            return html
        except Exception as e:
            logger.error(f"Error load check: {e}")
            return None

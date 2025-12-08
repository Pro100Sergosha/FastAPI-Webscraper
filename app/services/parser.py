import re
from typing import Any, Dict

from bs4 import BeautifulSoup
from markdownify import markdownify as md

from app.services.base import BaseParserService


class HtmlToMarkdownParser(BaseParserService):
    def __init__(self):
        self.TAGS_TO_REMOVE = [
            "script",
            "style",
            "noscript",
            "iframe",
            "header",
            "footer",
            "nav",
            "aside",
            "form",
            "svg",
            "button",
            "input",
            "img",
        ]

    async def parse(self, html: str) -> Dict[str, Any]:
        """
        Essential pipeline: HTML -> Clean HTML -> Markdown
        """
        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string if soup.title else "No Title"
        metadata = self._extract_metadata(soup)

        cleaned_soup = await self.clean(soup)

        markdown_content = md(str(cleaned_soup), heading_style="ATX", strip=["a"])

        clean_markdown = self._post_process_markdown(markdown_content)

        return {"title": title, "metadata": metadata, "content": clean_markdown}

    async def clean(self, soup: BeautifulSoup) -> BeautifulSoup:
        """
        Clean DOM-tree.
        Remove duplicate content (headers, footers, navigation)
        """
        for tag in soup(self.TAGS_TO_REMOVE):
            tag.decompose()

        for tag in soup.find_all(["div", "span"]):
            if not tag.get_text(strip=True) and not tag.find("img"):
                tag.decompose()

        for tag in soup.select(".ad, .advertisement, .cookie-banner"):
            tag.decompose()

        return soup

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extracts description and keywords for RAG"""
        meta = {}
        if description := soup.find("meta", attrs={"name": "description"}):
            meta["description"] = description.get("content", "")
        if keywords := soup.find("meta", attrs={"name": "keywords"}):
            meta["keywords"] = keywords.get("content", "")
        return meta

    def _post_process_markdown(self, text: str) -> str:
        return re.sub(r"\n{3,}", "\n\n", text).strip()

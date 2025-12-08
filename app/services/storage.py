import os
from urllib.parse import urlparse

import aiofiles

from app.services.base import BaseStorageBackend


class FileSystemStorage(BaseStorageBackend):
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    async def save(self, filename: str, content: str) -> None:
        filepath = os.path.join(self.base_path, filename)
        async with aiofiles.open(filepath, "w", encoding="utf-8") as f:
            await f.write(content)

    async def retrieve(self, key: str) -> str:
        pass

    @staticmethod
    def generate_filename(url: str, extension: str = ".html") -> str:
        """Generate filename from raw URL"""
        path = urlparse(url).path.strip("/")
        name = path.replace("/", "_").replace("-", "_")
        if not name:
            name = "index"
        return f"{name}{extension}"

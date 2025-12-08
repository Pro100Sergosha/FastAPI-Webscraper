import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class BaseStorageBackend(ABC):
    """Interface for storage backend"""

    @abstractmethod
    async def save(self, filename: str, content: str) -> None:
        """Save content to storage"""
        pass

    @abstractmethod
    async def retrieve(self, key: str) -> Optional[str]:
        """Retrieve content by key"""
        pass


class BaseParserService(ABC):
    """Interface for parsing (HTML -> Markdown)"""

    @abstractmethod
    async def parse(self, html: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

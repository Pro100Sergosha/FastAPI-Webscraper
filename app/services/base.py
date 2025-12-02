from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


# --- Parsing Interface ---
# [cite_start]See page 4 of PDF [cite: 79-87]
class BaseParserService(ABC):

    @abstractmethod
    async def parse(self, html: str) -> Dict[str, Any]:
        """Parse HTML and extract content"""
        pass

    @abstractmethod
    async def clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean extracted data"""
        pass


# --- Storage Interface ---
class BaseStorageBackend(ABC):

    @abstractmethod
    async def save(
        self, key: str, content: str, metadata: Dict[str, Any] = None
    ) -> None:
        """Save content with metadata"""
        pass

    @abstractmethod
    async def retrieve(self, key: str) -> Optional[str]:
        """Retrieve content by key"""
        pass

from abc import ABC, abstractmethod
from typing import Dict


class AIClient(ABC):
    """
    Abstract base class defining the interface for AI clients.
    """

    @abstractmethod
    async def analyze_text(self, text: str) -> Dict[str, str]:
        """
        Analyzes the given text and returns a dictionary with the analysis results.

        :param text: The text to be analyzed.
        :return: A dictionary containing keys like 'topic', 'language', 'sentiment', and 'text'.
        """
        pass

from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    name: str

    @abstractmethod
    async def run(self, input_data: dict) -> dict:
        """Execute agent logic and return structured JSON output."""
        ...

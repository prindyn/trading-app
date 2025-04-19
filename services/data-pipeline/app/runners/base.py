from abc import ABC, abstractmethod
from typing import List


class BasePipelineRunner(ABC):
    @abstractmethod
    async def run(self, pipelines: List) -> None:
        """Run pipelines in parallel."""
        raise NotImplementedError

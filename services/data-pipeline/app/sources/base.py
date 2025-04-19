from abc import ABC, abstractmethod
from typing import List, Any
from app.core.logger import logger


class BaseSource(ABC):
    base_url: str = ""
    name: str = "base"
    pipeline_client_map = {}

    def __init__(self, name: str = ""):
        self.name = f"{self._name}_{name}" if name else self._name

    def normalize_interval(self, interval: Any) -> int:
        """
        Convert exchange-specific interval format to minutes.
        Should be overridden by each exchange subclass if needed.
        """
        return int(interval)

    def get_client_cls(self, pipeline: Any) -> Any:
        """
        Return the client instance for a given pipeline.
        """
        if not self.pipeline_client_map:
            logger.warning(
                f"No pipeline client map defined for this source: {self.name}"
            )
        return self.pipeline_client_map.get(pipeline.__name__)

    @abstractmethod
    async def get_active_pairs(self) -> List[str]:
        """
        Must return a list of active trading pairs.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_intervals(self) -> List[str]:
        """
        Must return a list of intervals to fetch data for.
        """
        raise NotImplementedError

    @property
    def _name(self) -> str:
        """
        Returns the name of the source based on class name.
        """
        return self.__class__.__name__.replace("Source", "").lower()


class BaseExchange(BaseSource):
    pass

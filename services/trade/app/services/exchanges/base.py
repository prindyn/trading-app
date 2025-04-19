import logging
import inspect
import httpx

from abc import ABC, abstractmethod
from typing import Literal, Set

from datalib.decorators.http import cache_response_async

logger = logging.getLogger(__name__)


class BaseExchange(ABC):
    exchange_key: str
    cache: bool

    def __init__(self, exchange_id: str, cache: bool = True):
        from datalib.config import get_exchange_config

        self.cache = cache
        exchange_key = self.exchange_key
        config = get_exchange_config(exchange_key)
        if not config:
            raise ValueError(f"Config for exchange '{exchange_key}' not found.")
        config = config.copy()
        config["name"] = exchange_key

        self.config = config
        self._id = exchange_id
        self._name = exchange_key

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    async def fetch_symbols(
        self, market_type: Literal["spot", "futures"]
    ) -> Set[str]: ...

    def __cache_name(self):
        return f"{inspect.stack()[2].function}_{self.id}"

    @cache_response_async(name=__cache_name)
    async def _get_json_from_url(self, url: str) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"[{self.name}] Failed to fetch from {url}: {e}")
            return {}

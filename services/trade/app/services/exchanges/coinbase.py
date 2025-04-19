import logging
from typing import Literal, Set
from .base import BaseExchange

logger = logging.getLogger(__name__)


class CoinbaseExchange(BaseExchange):
    exchange_key = "coinbase"

    def __init__(self, exchange_id: str = None):
        super().__init__(exchange_id=exchange_id)

    async def fetch_symbols(self, market_type: Literal["spot", "futures"]) -> Set[str]:
        """
        Fetch tradable symbol IDs from Coinbase for the given market type.

        :param market_type: 'spot' only (Coinbase doesn't support futures in this integration)
        :return: set of trading pair strings (e.g., "BTC-USD")
        """
        if market_type != "spot":
            logger.warning(f"[Coinbase] Market type '{market_type}' not supported.")
            return set()

        try:
            url = self.config["base_url"] + self.config["endpoints"]["products"]
        except KeyError:
            logger.error("[Coinbase] Missing 'products' endpoint in config.")
            return set()

        try:
            data = await self._get_json_from_url(url)
        except Exception as e:
            logger.error(f"[Coinbase] Failed to fetch products from {url}: {e}")
            return set()

        return {
            product["id"].upper().replace("-", "")
            for product in data
            if product.get("status", "").lower() == "online"
        }

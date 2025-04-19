import logging
from typing import Literal, Set
from .base import BaseExchange

logger = logging.getLogger(__name__)


class BinanceExchange(BaseExchange):
    exchange_key = "binance"

    def __init__(self, exchange_id: str = None):
        super().__init__(exchange_id=exchange_id)

    async def fetch_symbols(self, market_type: Literal["spot", "futures"]) -> Set[str]:
        """
        Fetch tradable symbol IDs from Binance for the given market type.

        :param market_type: 'spot' or 'futures'
        :return: set of trading pair strings (e.g., "BTCUSDT")
        """
        endpoint_key = {
            "spot": "exchange_info",
            "futures": "futures_exchange_info",
        }.get(market_type)

        if not endpoint_key:
            logger.error(f"[Binance] Unsupported market type: {market_type}")
            return set()

        try:
            url = self.config["base_url"] + self.config["endpoints"][endpoint_key]
        except KeyError:
            logger.error(f"[Binance] Missing endpoint config for '{endpoint_key}'")
            return set()

        try:
            data = await self._get_json_from_url(url)
        except Exception as e:
            logger.error(f"[Binance] Failed to fetch symbols from {url}: {e}")
            return set()

        return {
            s["symbol"].upper()
            for s in data.get("symbols", [])
            if s.get("status") == "TRADING"
        }


class BinanceUSExchange(BinanceExchange):
    exchange_key = "binance_us"

    def __init__(self, exchange_id: str = None):
        super().__init__(exchange_id=exchange_id)

import logging
from typing import Literal, Set
from .base import BaseExchange

logger = logging.getLogger(__name__)


class KrakenExchange(BaseExchange):
    exchange_key = "kraken"

    def __init__(self, exchange_id: str = None):
        super().__init__(exchange_id=exchange_id)

    async def fetch_symbols(self, market_type: Literal["spot", "futures"]) -> Set[str]:
        """
        Fetch tradable symbol IDs from Kraken for the given market type.

        Note: Kraken REST API currently supports spot market data only.
        """
        if market_type != "spot":
            logger.warning(f"[Kraken] Market type '{market_type}' is not supported.")
            return set()

        try:
            url = self.config["base_url"] + self.config["endpoints"]["asset_pairs"]
        except KeyError:
            logger.error("[Kraken] Missing 'asset_pairs' endpoint in config.")
            return set()

        try:
            data = await self._get_json_from_url(url)
        except Exception as e:
            logger.error(f"[Kraken] Failed to fetch asset pairs from {url}: {e}")
            return set()

        if "result" not in data:
            logger.error("[Kraken] Unexpected response structure: 'result' missing.")
            return set()

        # Extract only live trading pairs
        return {
            pair_name.upper()
            for pair_name, pair_info in data["result"].items()
            if not pair_info.get("wsname", "").startswith(
                "."
            )  # skip dark pool or inactive
        }

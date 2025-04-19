from .base import BaseExchange
from typing import Dict, List
from app.clients.okx_ohlcv import OKXOHLCVClient

INTERVAL_MAPPING = {
    "1m": 1,
    "5m": 5,
    "15m": 15,
    "30m": 30,
    "1H": 60,
    "4H": 240,
    "1D": 1440,
    "1W": 10080,
    "1M": 43200,
}


class OKXExchange(BaseExchange):
    base_url = "https://www.okx.com"
    pipeline_client_map = {
        "OHLCPipeline": OKXOHLCVClient,
    }

    async def get_active_pairs(self) -> List[str]:
        return ["BTC-USDT", "ETH-USDT", "ETH-BTC"]

    async def get_intervals(self) -> List[str]:
        return INTERVAL_MAPPING.keys()

    def normalize_interval(self, interval):
        return INTERVAL_MAPPING.get(interval, 0)

    async def fetch_ohlcv_data(self, payload: Dict) -> List[Dict]:
        """
        Use OKXOHLCVClient to fetch and normalize OHLCV data.

        :param payload: Dictionary with 'symbol', 'interval', etc.
        :return: List of normalized OHLCV entries
        """
        client = OKXOHLCVClient(base_url=self.base_url)
        return await client.fetch_data(payload)

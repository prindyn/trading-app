from .base import BaseExchange
from typing import Dict, List
from app.clients.kraken_ohlcv import KrakenOHLCVClient
from app.clients.kraken_ticker import KrakenTickerClient


class KrakenExchange(BaseExchange):
    base_url = "https://api.kraken.com"
    pipeline_client_map = {
        "OHLCPipeline": KrakenOHLCVClient,
        "TickerPipeline": KrakenTickerClient,
    }

    async def get_active_pairs(self) -> List[str]:
        return ["XBTUSD", "ETHUSD", "ETHXBT"]

    async def get_intervals(self) -> List[int]:
        return [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]

    def normalize_interval(self, interval):
        return int(interval)

    async def fetch_ohlcv_data(self, payload: Dict) -> List[Dict]:
        """
        Use KrakenOHLCVClient to fetch and normalize OHLCV data.

        :param payload: Dictionary with 'symbol', 'interval', etc.
        :return: List of normalized OHLCV entries
        """
        client = KrakenOHLCVClient(base_url=self.base_url)
        return await client.fetch_data(payload)

    async def fetch_ticker_data(self, payload: Dict) -> List[Dict]:
        """
        Use KrakenTickerClient to fetch and normalize Ticker data.

        :param payload: Dictionary with 'symbol', 'interval', etc.
        :return: List of normalized Ticker entries
        """
        client = KrakenTickerClient(base_url=self.base_url)
        return await client.fetch_data(payload)

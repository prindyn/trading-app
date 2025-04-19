# --- app/services/kraken_ohlcv_service.py ---
import httpx
from typing import List, Dict
from app.core.logger import logger


class KrakenOHLCService:
    BASE_URL = "https://api.kraken.com/0/public/OHLC"

    def __init__(self, pair: str = "XBTUSD", interval: int = 1, since: int = None):
        self.pair = pair
        self.interval = interval
        self.since = since  # Optional UNIX timestamp (seconds)

    def build_params(self) -> Dict:
        """
        Build the query parameters for the Kraken OHLC API request.
        """
        params = {
            "pair": self.pair,
            "interval": self.interval,
        }
        if self.since:
            params["since"] = self.since
        return params

    async def fetch_raw(self) -> Dict:
        """
        Fetch raw OHLCV response from Kraken API.
        """
        params = self.build_params()
        logger.info(f"Fetching OHLCV from Kraken: {params}")

        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()

    def extract_data_key(self, raw: Dict) -> str:
        """
        Extract the data key (Kraken uses pair code as key).
        """
        return next((k for k in raw.get("result", {}) if k != "last"), None)

    def parse_ohlcv(self, raw: Dict) -> List[Dict]:
        """
        Parse raw OHLCV data into a normalized format.
        """
        key = self.extract_data_key(raw)
        rows = raw.get("result", {}).get(key, [])

        parsed = [
            {
                "timestamp": int(r[0]),
                "open": float(r[1]),
                "high": float(r[2]),
                "low": float(r[3]),
                "close": float(r[4]),
                "volume": float(r[6]),
                "pair": self.pair,
            }
            for r in rows
        ]
        return parsed

    async def fetch_ohlcv_data(self) -> List[Dict]:
        """
        Full fetch & parse method used by pipelines.
        """
        try:
            raw = await self.fetch_raw()
            parsed = self.parse_ohlcv(raw)
            logger.info(f"Parsed {len(parsed)} OHLCV entries from Kraken")
            return parsed
        except Exception as e:
            logger.error(f"Failed to fetch OHLCV from Kraken: {e}")
            raise

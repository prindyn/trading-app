from .base import BasePipeline
from typing import List, Dict, Any

REQUIRED_FIELDS = {
    "timestamp",
    "symbol",
    "price",
    "bid",
    "ask",
    "volume",
}


class TickerPipeline(BasePipeline):
    name = "TickerPipeline"

    async def fetch_data(self) -> List[Dict[str, Any]]:
        """
        Fetch Ticker data from the configured source.
        """
        return await self.source.fetch_ticker_data(self.config)

    def validate_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Ensures the data is a list of dictionaries with required ticker fields.

        :param data: Fetched data
        :raises ValueError: if structure is invalid
        """
        if not isinstance(data, list):
            raise ValueError("Expected a list of ticker data entries")

        for entry in data:
            if not isinstance(entry, dict):
                raise ValueError("Each ticker entry must be a dictionary")
            missing = REQUIRED_FIELDS - entry.keys()
            if missing:
                raise ValueError(f"Missing fields in ticker entry: {missing}")

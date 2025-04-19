from app.pipelines.base import BasePipeline
from typing import List, Dict, Any

REQUIRED_FIELDS = {
    "timestamp",
    "price",
    "volume",
    "side",
    "pair",
    "trade_id",
}


class RecentTradesPipeline(BasePipeline):
    name = "RecentTradesPipeline"

    async def fetch_data(self) -> List[Dict[str, Any]]:
        """
        Fetch recent trade data from the configured source.
        """
        return await self.source.fetch_recent_trades_data(self.config)

    def validate_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Ensures the data is a list of dictionaries with required trade fields.

        :param data: Fetched data
        :raises ValueError: if structure is invalid
        """
        if not isinstance(data, list):
            raise ValueError("Expected a list of recent trades")

        for entry in data:
            if not isinstance(entry, dict):
                raise ValueError("Each trade entry must be a dictionary")
            missing = REQUIRED_FIELDS - entry.keys()
            if missing:
                raise ValueError(f"Missing fields in trade entry: {missing}")

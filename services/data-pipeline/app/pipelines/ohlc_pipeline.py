from .base import BasePipeline
from typing import List, Dict, Any
from datetime import datetime

REQUIRED_FIELDS = {
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "pair",
}


class OHLCPipeline(BasePipeline):
    name = "OHLCPipeline"

    async def fetch_data(self) -> List[Dict[str, Any]]:
        """
        Fetch OHLCV data from the configured source.
        """
        return await self.source.fetch_ohlcv_data(self.config)

    def validate_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Ensures the data is a list of dictionaries with required OHLCV fields.

        :param data: Fetched data
        :raises ValueError: if structure is invalid
        """
        if not isinstance(data, list):
            raise ValueError("Expected a list of OHLCV data entries")

        for entry in data:
            if not isinstance(entry, dict):
                raise ValueError("Each OHLCV entry must be a dictionary")
            missing = REQUIRED_FIELDS - entry.keys()
            if missing:
                raise ValueError(f"Missing fields in OHLCV entry: {missing}")

    def should_run(self) -> bool:
        interval = self.config.get("interval")
        normalized = self.source.normalize_interval(interval)
        now = datetime.utcnow()

        if normalized == 1:
            return True
        elif normalized == 5:
            return now.minute % 5 == 0
        elif normalized == 15:
            return now.minute % 15 == 0
        elif normalized == 30:
            return now.minute % 30 == 0
        elif normalized == 60:
            return now.minute == 0
        elif normalized == 240:
            return now.hour % 4 == 0 and now.minute == 0
        elif normalized == 1440:
            return now.hour == 0 and now.minute == 0

        return True

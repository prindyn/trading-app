from app.clients.base import BaseClient
from typing import Dict, List, Any


class OKXOHLCVClient(BaseClient):
    endpoint = "/api/v5/market/candles"
    request_fields = {"instId": "symbol", "bar": "interval"}

    def parse_data(self, raw: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse raw OHLCV data into a normalized format.
        """
        rows = raw.get("data", [])

        parsed = [
            {
                "timestamp": int(int(row[0]) / 1000),  # OKX returns ms
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": float(row[5]),
                "pair": self._params.get("instId"),
            }
            for row in rows
        ]

        return parsed

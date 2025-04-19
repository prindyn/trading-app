from app.clients.base import BaseClient
from typing import Dict, List, Any


class KrakenOHLCVClient(BaseClient):
    endpoint = "/0/public/OHLC"
    request_fields = {"pair": "symbol", "interval": "interval"}

    def _extract_data_key(self, raw: Dict[str, Any]) -> str:
        """
        Extract the data key (Kraken uses pair code as key).
        """
        return next((k for k in raw.get("result", {}) if k != "last"), None)

    def parse_data(self, raw: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse raw OHLCV data into a normalized format.
        """
        key = self._extract_data_key(raw)
        rows = raw.get("result", {}).get(key, [])

        parsed = [
            {
                "timestamp": int(r[0]),
                "open": float(r[1]),
                "high": float(r[2]),
                "low": float(r[3]),
                "close": float(r[4]),
                "volume": float(r[6]),
                "pair": self._params.get("pair"),
            }
            for r in rows
        ]

        return parsed

from app.clients.base import BaseClient
from typing import Dict, List, Any


class KrakenTickerClient(BaseClient):
    endpoint = "/0/public/Ticker"
    request_fields = {"pair": "symbol"}

    def parse_data(self, raw: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse the raw Ticker response into a normalized format.
        """
        pair = self._params.get("pair")
        result = raw.get("result", {})
        key = next(iter(result))  # extract the first key under result
        info = result.get(key, {})

        parsed = [
            {
                "timestamp": int(
                    raw.get("timestamp", 0)
                ),  # Not included by default in Kraken Ticker API
                "symbol": pair,
                "price": float(info["c"][0]),
                "bid": float(info["b"][0]),
                "ask": float(info["a"][0]),
                "volume": float(info["v"][1]),
            }
        ]

        return parsed

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import Optional

COINGECKO_API = "https://api.coingecko.com/api/v3"


def prepare_fetch_args(
    symbol: str, interval: str, start: str, end: Optional[str] = None
) -> dict:
    if "-" not in symbol:
        raise ValueError("Expected symbol format like 'bitcoin-usd' or 'BITCOIN-USD'")

    symbol_id, vs_currency = symbol.lower().split("-")

    return {
        "symbol": symbol_id,
        "vs_currency": vs_currency,
        "interval": interval,
        "start": start,
        "end": end,
        "chunk_days": 30 if interval == "hourly" else 90,
    }


def fetch_cg_ohlcv(
    symbol: str = "bitcoin",
    vs_currency: str = "usd",
    interval: str = "hourly",
    start: str = "2023-01-01",
    end: Optional[str] = None,
    chunk_days: int = 30,
) -> pd.DataFrame:
    """
    Fetch OHLCV data from CoinGecko using /market_chart/range.
    Only 'hourly' is practically supported. Other intervals will be ignored with a warning.
    """
    if interval != "hourly":
        print(
            "[coingecko] Warning: CoinGecko only supports hourly granularity for /range. Returning hourly data."
        )

    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d") if end else datetime.utcnow()

    all_chunks = []

    while start_dt < end_dt:
        to_dt = min(start_dt + timedelta(days=chunk_days), end_dt)
        from_ts = int(start_dt.timestamp())
        to_ts = int(to_dt.timestamp())

        url = f"{COINGECKO_API}/coins/{symbol}/market_chart/range"
        params = {"vs_currency": vs_currency, "from": from_ts, "to": to_ts}
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MyBot/1.0; +https://mydomain.com/bot)"
        }

        print(
            f"[coingecko] Fetching {symbol} from {start_dt.date()} to {to_dt.date()}..."
        )
        for attempt in range(3):
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                break
            time.sleep(2)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
        df["volume"] = [v[1] for v in data["total_volumes"]]
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["open"] = df["price"]
        df["high"] = df["price"]
        df["low"] = df["price"]
        df["close"] = df["price"]
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]

        all_chunks.append(df)
        time.sleep(1.2)  # Rate limiting

        start_dt = to_dt

    return pd.concat(all_chunks).reset_index(drop=True)

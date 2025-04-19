from binance.client import Client
import pandas as pd
from datetime import datetime


def prepare_fetch_args(
    symbol: str, interval: str, start: str, end: str | None = None
) -> dict:
    binance_interval_map = {
        "1m": Client.KLINE_INTERVAL_1MINUTE,
        "5m": Client.KLINE_INTERVAL_5MINUTE,
        "15m": Client.KLINE_INTERVAL_15MINUTE,
        "30m": Client.KLINE_INTERVAL_30MINUTE,
        "1h": Client.KLINE_INTERVAL_1HOUR,
        "4h": Client.KLINE_INTERVAL_4HOUR,
        "1d": Client.KLINE_INTERVAL_1DAY,
    }
    return {
        "symbol": symbol.upper(),
        "interval": binance_interval_map.get(interval, Client.KLINE_INTERVAL_1HOUR),
        "start": start,
        "end": end or datetime.utcnow().strftime("%Y-%m-%d"),
    }


def fetch_bn_ohlcv(symbol: str, interval: str, start: str, end: str):
    client = Client()
    klines = client.get_historical_klines(symbol, interval, start, end)

    df = pd.DataFrame(
        klines,
        columns=[
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "trades",
            "taker_buy_base",
            "taker_buy_quote",
            "ignore",
        ],
    )

    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df.astype(
        {"open": float, "high": float, "low": float, "close": float, "volume": float}
    )
    return df

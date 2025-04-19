import yfinance as yf
from datetime import datetime, timedelta


def prepare_fetch_args(
    symbol: str, interval: str, start: str, end: str | None = None
) -> dict:
    # YFinance supports max 730 days of intraday data
    if interval in ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"]:
        max_start = datetime.utcnow() - timedelta(days=729)
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        if start_dt < max_start:
            print(
                f"[yfinance] Warning: Adjusting start date to {max_start.date()} due to Yahoo limits"
            )
            start = max_start.strftime("%Y-%m-%d")

    return {
        "symbol": symbol,
        "interval": interval,
        "start": start,
        "end": end,
    }


def fetch_yf_ohlcv(symbol: str, interval: str, start: str, end: str):
    df = yf.download(symbol, interval=interval, start=start, end=end)
    # Flatten multi-index or format suffixes if needed
    df.columns = [
        f"{c[0].lower()}_{c[1].lower()}" if isinstance(c, tuple) else c.lower()
        for c in df.columns
    ]
    df = df.reset_index()
    # Force lowercase and handle timestamp mapping
    rename_map = {}
    for col in df.columns:
        col_lc = col.lower()
        if col_lc in ["datetime", "date"]:
            rename_map[col] = "timestamp"
        for target in ["open", "high", "low", "close", "volume"]:
            if target in col_lc:
                rename_map[col] = target
    df.rename(columns=rename_map, inplace=True)
    expected = ["timestamp", "open", "high", "low", "close", "volume"]
    missing = [col for col in expected if col not in df.columns]
    if missing:
        raise KeyError(f"Missing columns from Yahoo response: {missing}")

    return df[expected]

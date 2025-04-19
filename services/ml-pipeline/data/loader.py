"""
Usage Examples for fetch-data CLI:

# CoinGecko
python cli.py fetch-data --source=coingecko --symbol=BITCOIN-USD --interval=hourly

# Yahoo Finance
python cli.py fetch-data --source=yfinance --symbol=BTC-USD --interval=1h

# Binance
python cli.py fetch-data --source=binance --symbol=BTCUSDT --interval=1h

Optional:
  --start=YYYY-MM-DD   # default: 2023-01-01
  --end=YYYY-MM-DD     # optional, default: now

Notes:
- CoinGecko symbols must be lowercase coin IDs (e.g., 'bitcoin', 'ethereum')
- yfinance symbols use dash format (e.g., 'BTC-USD', 'ETH-USD'), intraday limited to ~730 days
- Binance symbols use uppercase pairs (e.g., 'BTCUSDT'), and support many intervals
"""

import config
import pandas as pd
from pathlib import Path


def load_training_data(model_name: str) -> pd.DataFrame:
    filename = config.MODEL_DATA_FILES.get(model_name)
    if not filename:
        raise ValueError(f"No data file configured for model: {model_name}")

    path = config.TRAINING_DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Training data file not found: {path}")

    return pd.read_csv(path, parse_dates=["timestamp"])


def fetch_data(source: str = "binance", **kwargs):
    if source not in config.DATA_SOURCE_FETCHERS:
        raise ValueError(f"Unsupported data source: {source}")

    prepare_args, fetch_fn = config.DATA_SOURCE_FETCHERS[source]
    args = prepare_args(
        kwargs.get("symbol"),
        kwargs.get("interval"),
        kwargs.get("start"),
        kwargs.get("end"),
    )
    return fetch_fn(**args)


def load_and_save_data(source: str, symbol: str, interval: str, start: str, end: str):
    df = fetch_data(source, symbol=symbol, interval=interval, start=start, end=end)

    filename = f"{symbol.replace('-', '').lower()}_{interval}.csv"
    save_path = Path("data/source/") / filename
    save_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(save_path, index=False)

    print(f"[data] Saved {len(df)} rows to {save_path}")
    return df

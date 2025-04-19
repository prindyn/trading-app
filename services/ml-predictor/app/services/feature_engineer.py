import pandas as pd
import numpy as np
from app.database.schemas import Candle
from typing import List


def extract_features(candles: List[Candle]) -> np.ndarray:
    df = pd.DataFrame([c.dict() for c in candles])
    df["returns"] = df["close"].pct_change()
    df["volatility"] = df["returns"].rolling(window=20).std()
    df["momentum"] = df["close"] - df["close"].rolling(window=10).mean()
    df = df.dropna()
    features = df[["returns", "volatility", "momentum"]].values[-1:]
    return features

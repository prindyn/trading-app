from pydantic import BaseModel, Field
from typing import List


class Candle(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float


class PredictionRequest(BaseModel):
    candles: List[Candle] = Field(..., min_items=100)


class PredictionResponse(BaseModel):
    expected_gain: float
    confidence: float
    direction: str  # "long" or "short"

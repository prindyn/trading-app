from pydantic import BaseModel
from typing import Literal, List, Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


# ===== ASSET =====
class AssetOut(BaseModel):
    id: UUID
    symbol: str
    name: str
    image: str
    is_fiat: bool

    class Config:
        from_attributes = True


# ===== TRADE =====
class TradeCreate(BaseModel):
    symbol: str
    price: float
    quantity: float


class TradeOut(TradeCreate):
    id: UUID

    class Config:
        from_attributes = True


# ===== TRADE PAIR =====
class TradePairCreate(BaseModel):
    base_symbol: str
    quote_symbol: str
    exchange: str
    type: Literal["spot", "futures"]
    is_active: bool


class TradePairOut(BaseModel):
    base_symbol: str
    quote_symbol: str
    image: str
    type: Literal["spot", "futures"]


# ===== EXCHANGE =====
class ExchangeOut(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


# ===== SYNC TASKS =====
class PairInput(BaseModel):
    base_symbol: str
    quote_symbol: str


class SyncRequest(BaseModel):
    exchange_id: str
    market_type: Literal["spot", "futures"]
    pair_data: List[PairInput] = []


# ===== GENERAL =====
class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    total: int

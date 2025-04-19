from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import (
    AssetOut,
    TradeOut,
    TradePairOut,
    TradeCreate,
    ExchangeOut,
    PaginatedResponse,
)
from app.models.crud import (
    create_trade,
    get_all_trades,
    get_trade_by_id,
    get_paginated_assets,
    get_paginated_trade_pairs,
    get_all_exchanges,
)
from app.core.database import get_session
from typing import List
from uuid import UUID

router = APIRouter()


@router.get("/exchanges", response_model=list[ExchangeOut])
async def list_exchanges(db: AsyncSession = Depends(get_session)):
    return await get_all_exchanges(db)


@router.get("/pairs", response_model=PaginatedResponse[TradePairOut])
async def list_trade_pairs(
    exchange_id: UUID = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_session),
):
    return await get_paginated_trade_pairs(
        db=db,
        exchange_id=exchange_id,
        limit=limit,
        offset=offset,
    )


# @router.post("/", response_model=TradeOut)
# async def create(trade: TradeCreate, db: AsyncSession = Depends(get_session)):
#     return await create_trade(db, trade)


# @router.get("/{trade_id}", response_model=TradeOut)
# async def read_one(trade_id: int, db: AsyncSession = Depends(get_session)):
#     trade = await get_trade_by_id(db, trade_id)
#     if not trade:
#         raise HTTPException(status_code=404, detail="Trade not found")
#     return trade


@router.get("/assets", response_model=PaginatedResponse[AssetOut])
async def list_assets(
    fiat_only: bool = Query(False),
    search: str = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_session),
):
    return await get_paginated_assets(
        db=db,
        fiat_only=fiat_only,
        search=search,
        limit=limit,
        offset=offset,
    )

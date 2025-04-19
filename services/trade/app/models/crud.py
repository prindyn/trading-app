from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import Select, literal
from datalib.decorators.database import paginated
from app.models.schemas import (
    TradeCreate,
    TradeOut,
    TradePairCreate,
    TradePairOut,
    AssetOut,
    ExchangeOut,
)
from app.models.tables import (
    Trade,
    TradePair,
    Asset,
    Exchange,
    PairAvailability,
)
from app.models.aliases import base, quote
from typing import Optional
from uuid import UUID


async def create_trade(db: AsyncSession, trade: TradeCreate):
    new_trade = Trade(**trade.dict())
    db.add(new_trade)
    await db.commit()
    await db.refresh(new_trade)
    return new_trade


async def get_trade_by_id(db: AsyncSession, trade_id: int):
    result = await db.execute(select(Trade).filter_by(id=trade_id))
    return result.scalar_one_or_none()


async def get_all_trades(db: AsyncSession, limit: int = 100):
    result = await db.execute(select(Trade).limit(limit))
    return result.scalars().all()


async def get_all_exchanges(db: AsyncSession) -> list[ExchangeOut]:
    result = await db.execute(select(Exchange))
    exchanges = result.scalars().all()
    return [ExchangeOut.model_validate(e) for e in exchanges]


@paginated(AssetOut, search_fields=[Asset.symbol, Asset.name])
async def get_paginated_assets(
    db: AsyncSession,
    fiat_only: bool = False,
) -> Select:
    stmt = select(Asset).select_from(Asset)
    if fiat_only:
        stmt = stmt.where(Asset.is_fiat.is_(True))
    return stmt


@paginated(TradePairOut, search_fields=[base.symbol, quote.symbol], scalars=False)
async def get_paginated_trade_pairs(
    db: AsyncSession,
    exchange_id: Optional[UUID] = None,
    fiat_only: Optional[bool] = None,
) -> Select:
    stmt = (
        select(
            base.symbol.label("base_symbol"),
            quote.symbol.label("quote_symbol"),
            quote.image.label("image"),
            PairAvailability.type.label("type"),
            PairAvailability.is_active.label("is_active"),
        )
        .select_from(PairAvailability)
        .join(TradePair, PairAvailability.trade_pair_id == TradePair.id)
        .join(base, TradePair.base_asset_id == base.id)
        .join(quote, TradePair.quote_asset_id == quote.id)
    )

    if exchange_id:
        stmt = stmt.where(PairAvailability.exchange_id == exchange_id)

    if fiat_only is not None:
        stmt = stmt.where(quote.is_fiat == fiat_only)

    return stmt

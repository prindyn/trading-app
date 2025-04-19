import uuid
import logging
from typing import Literal, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session_async
from app.services.exchanges.base import BaseExchange
from app.models.tables import Asset, TradePair, PairAvailability

logger = logging.getLogger(__name__)


class PairAvailabilitySyncService:
    def __init__(self): ...

    async def sync(
        self,
        exchange: BaseExchange,
        market_type: Literal["spot", "futures"],
        pair_data: List[dict] = [],
    ):
        available_symbols = await exchange.fetch_symbols(market_type)
        added = 0
        skipped = 0

        if not pair_data:
            import json

            with open("seed/data/trade_pair.json", "r") as f:
                pair_data = json.load(f)

        async with get_session_async() as db:
            for pair in pair_data:
                base_symbol = pair["base_symbol"].upper()
                quote_symbol = pair["quote_symbol"].upper()
                symbol_id = f"{base_symbol}{quote_symbol}"

                base_asset = await self._get_asset_by_symbol(db, base_symbol)
                quote_asset = await self._get_asset_by_symbol(db, quote_symbol)

                if not base_asset or not quote_asset:
                    logger.warning(
                        f"Skipping unknown asset pair: {base_symbol}/{quote_symbol}"
                    )
                    skipped += 1
                    continue

                trade_pair = await self._get_or_create_trade_pair(
                    db, base_asset.id, quote_asset.id
                )

                stmt = select(PairAvailability).where(
                    PairAvailability.trade_pair_id == trade_pair.id,
                    PairAvailability.exchange_id == exchange.id,
                    PairAvailability.type == market_type,
                )
                existing = (await db.execute(stmt)).scalar_one_or_none()
                is_active = symbol_id in available_symbols

                if not existing:
                    db.add(
                        PairAvailability(
                            id=uuid.uuid4(),
                            trade_pair_id=trade_pair.id,
                            exchange_id=exchange.id,
                            type=market_type,
                            is_active=is_active,
                        )
                    )
                    added += 1
                elif existing.is_active != is_active:
                    existing.is_active = is_active
                    added += 1

            await db.commit()

        logger.info(
            f"Pair sync complete for exchange {exchange.name} ({market_type}). "
            f"Added/Updated: {added}, Skipped: {skipped}"
        )

    async def _get_asset_by_symbol(self, db: AsyncSession, symbol: str) -> Asset | None:
        stmt = select(Asset).where(Asset.symbol == symbol)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_or_create_trade_pair(
        self, db: AsyncSession, base_id: str, quote_id: str
    ) -> TradePair:
        stmt = select(TradePair).where(
            TradePair.base_asset_id == base_id,
            TradePair.quote_asset_id == quote_id,
        )
        result = await db.execute(stmt)
        trade_pair = result.scalar_one_or_none()

        if trade_pair:
            return trade_pair

        trade_pair = TradePair(
            id=uuid.uuid4(),
            base_asset_id=base_id,
            quote_asset_id=quote_id,
        )
        db.add(trade_pair)
        await db.flush()
        return trade_pair

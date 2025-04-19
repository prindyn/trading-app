from fastapi import APIRouter, HTTPException
from app.models.schemas import SyncRequest
from app.services.pair_availability_sync import PairAvailabilitySyncService
from app.services.exchanges.factory import get_exchange_instance_by_id
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/sync/pairs", summary="Sync pair availability for an exchange")
async def sync_pairs(payload: SyncRequest):
    try:
        service = PairAvailabilitySyncService()
        exchange = await get_exchange_instance_by_id(payload.exchange_id)

        await service.sync(
            exchange=exchange,
            market_type=payload.market_type,
            pair_data=[pair.dict() for pair in payload.pair_data],
        )
        return {"detail": "Pair availability sync completed."}
    except Exception as e:
        logger.exception("Sync pair task failed")
        raise HTTPException(status_code=500, detail=str(e))

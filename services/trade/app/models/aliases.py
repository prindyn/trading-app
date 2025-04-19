from sqlalchemy.orm import aliased
from app.models.tables import (
    Trade,
    TradePair,
    Asset,
    Exchange,
    PairAvailability,
)

base = aliased(Asset)
quote = aliased(Asset)

import re
import logging
from typing import Optional
from sqlalchemy import select
from app.models.tables import Exchange
from app.core.database import get_session_async
from .binance_us import BINANCE_US_CONFIG
from .binance import BINANCE_CONFIG
from .coinbase import COINBASE_CONFIG
from .kraken import KRAKEN_CONFIG

logger = logging.getLogger(__name__)

EXCHANGE_CONFIGS = {
    "binance": BINANCE_CONFIG,
    "binance_us": BINANCE_US_CONFIG,
    "coinbase": COINBASE_CONFIG,
    "kraken": KRAKEN_CONFIG,
}


def _normalize_exchange_name(name: str) -> str:
    """
    Convert a human-readable exchange name to a config-friendly key.
    E.g., "Binance US" -> "binance_us"
    """
    if not name:
        return name
    return re.sub(r"\W+", "_", name.strip().lower())


def get_exchange_config(exchange: str, key_path: Optional[str] = None):
    """
    Retrieve config dictionary or nested value for an exchange.

    :param exchange: Exchange key like "binance"
    :param key_path: Optional dot-separated path, e.g. "endpoints.exchange_info"
    :return: config value or None
    """
    exchange_name = _normalize_exchange_name(exchange)
    config = EXCHANGE_CONFIGS.get(exchange_name)
    if config is None:
        logger.error(f"Exchange config '{exchange}' not found.")
        return None

    if not key_path:
        return config

    value = config
    for key in key_path.split("."):
        if not isinstance(value, dict) or key not in value:
            logger.error(f"Key path '{key_path}' not found in config for '{exchange}'")
            return None
        value = value[key]

    return value


async def get_exchange_config_by_id(
    exchange_id: str, key_path: Optional[str] = None
) -> dict | str | None:
    """
    Retrieve an exchange config or nested config value by exchange ID.

    :param exchange_id: UUID of the exchange from the DB
    :param key_path: Optional dot-separated path (e.g., 'endpoints.exchange_info')
    :return: Full config dict or specific nested value, or None
    """
    stmt = select(Exchange).where(Exchange.id == exchange_id)
    async with get_session_async() as db:
        result = await db.execute(stmt)
        exchange = result.scalar_one_or_none()

    if not exchange:
        logger.error(f"Exchange with ID '{exchange_id}' not found in DB.")
        return None

    exchange_name = _normalize_exchange_name(exchange.name)
    base_config = EXCHANGE_CONFIGS.get(exchange_name)

    if not base_config:
        logger.error(f"No config registered for exchange name '{exchange_name}'")
        return None

    config = base_config.copy()
    config["id"] = str(exchange.id)

    if not key_path:
        return config

    # Resolve dot-notated key path from local config copy
    value = config
    for key in key_path.split("."):
        if not isinstance(value, dict) or key not in value:
            logger.error(
                f"Key path '{key_path}' not found in config for '{exchange_name}'"
            )
            return None
        value = value[key]

    return value

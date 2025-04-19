from .coinbase import CoinbaseExchange
from .kraken import KrakenExchange
from .base import BaseExchange
from .binance import BinanceExchange, BinanceUSExchange
from datalib.config import get_exchange_config_by_id, _normalize_exchange_name

EXCHANGE_CLASS_MAP = {
    "binance": BinanceExchange,
    "binance_us": BinanceUSExchange,
    "coinbase": CoinbaseExchange,
    "kraken": KrakenExchange,
}


def get_exchange_instance_by_name(name: str) -> BaseExchange:
    cls = EXCHANGE_CLASS_MAP.get(name.lower())
    if not cls:
        raise ValueError(f"No exchange implementation for '{name}'")
    return cls()


async def get_exchange_instance_by_id(id: str) -> BaseExchange:
    name = await get_exchange_config_by_id(id, key_path="name")
    name = _normalize_exchange_name(name)
    if not name:
        raise ValueError(f"Could not resolve exchange name for ID: {id}")

    cls = EXCHANGE_CLASS_MAP.get(name)
    if not cls:
        raise ValueError(f"No exchange implementation for '{name}'")
    return cls(id)

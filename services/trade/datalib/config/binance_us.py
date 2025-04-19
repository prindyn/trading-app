BINANCE_US_CONFIG = {
    "name": "Binance US",
    "base_url": "https://api.binance.us",
    "futures_url": None,  # Binance US does not offer futures
    "endpoints": {
        "exchange_info": "/api/v3/exchangeInfo",
        "account": "/api/v3/account",
        "order": "/api/v3/order",
    },
    "features": ["spot"],  # No futures
    "rate_limit_per_minute": 1200,  # Same as Binance global
    "api_key_header": "X-MBX-APIKEY",
    "signature_required": True,
    "signature_type": "HMAC_SHA256",
}

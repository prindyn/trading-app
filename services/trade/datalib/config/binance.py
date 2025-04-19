BINANCE_CONFIG = {
    "name": "Binance",
    # "base_url": "https://api.binance.com",
    "base_url": "https://testnet.binance.vision",
    # "futures_url": "https://fapi.binance.com",
    "futures_url": "https://testnet.binancefuture.com",
    "endpoints": {
        "exchange_info": "/api/v3/exchangeInfo",
        "futures_exchange_info": "/fapi/v1/exchangeInfo",
        "account": "/api/v3/account",
        "order": "/api/v3/order",
    },
    "features": ["spot", "futures"],
    "rate_limit_per_minute": 1200,
    "api_key_header": "X-MBX-APIKEY",
    "signature_required": True,
    "signature_type": "HMAC_SHA256",
}

KRAKEN_CONFIG = {
    "name": "Kraken",
    "base_url": "https://api.kraken.com",
    "endpoints": {
        "asset_pairs": "/0/public/AssetPairs",
        "account_balance": "/0/private/Balance",
        "add_order": "/0/private/AddOrder",
    },
    "features": ["spot"],
    "rate_limit_per_minute": 60,
    "api_key_header": "API-Key",
    "signature_required": True,
    "signature_type": "HMAC_SHA512",
}

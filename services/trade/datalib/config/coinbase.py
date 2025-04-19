COINBASE_CONFIG = {
    "name": "Coinbase",
    "base_url": "https://api.exchange.coinbase.com",
    "endpoints": {
        "products": "/products",  # list trading pairs
        "accounts": "/accounts",
        "orders": "/orders",
    },
    "features": ["spot"],
    "rate_limit_per_minute": 10000,
    "api_key_header": "CB-ACCESS-KEY",
    "signature_required": True,
    "signature_type": "HMAC_SHA256",
    "additional_headers": [
        "CB-ACCESS-TIMESTAMP",
        "CB-ACCESS-PASSPHRASE",
        "CB-ACCESS-SIGN",
    ],
}

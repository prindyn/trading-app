import uuid
import requests
import json
from pathlib import Path
from urllib.parse import urlparse, urlunparse

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

output_file = DATA_DIR / "asset.json"

# Load existing assets (if any)
existing_assets = []
existing_symbols = set()

if output_file.exists():
    with open(output_file, "r") as f:
        try:
            existing_assets = json.load(f)
            existing_symbols = {a["symbol"].upper() for a in existing_assets}
        except Exception:
            ...

# Fetch tickers from CoinGecko Binance exchange
response = requests.get("https://api.coingecko.com/api/v3/exchanges/binance_us")
tickers = response.json().get("tickers", [])

# Collect all unique base and target symbols
symbols = set()
for t in tickers:
    symbols.add(t["base"].upper())
    symbols.add(t["target"].upper())

# Remove already existing symbols
new_symbols = symbols - existing_symbols

# Fetch metadata for all known coins
coin_response = requests.get(
    "https://api.coingecko.com/api/v3/coins/markets",
    params={
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": 1,
    },
)
coin_data = coin_response.json()

# Map: symbol -> {name, image}
try:
    coin_lookup = {
        coin["symbol"].upper(): {
            "name": coin["name"],
            "image": coin["image"].split("?")[0] if "image" in coin else "",
        }
        for coin in coin_data
    }
except:
    ...

# Add only new symbols with available metadata
added = 0
for symbol in new_symbols:
    if symbol not in coin_lookup:
        continue  # Skip unknown or obscure symbols not in coin list

    data = coin_lookup[symbol]
    existing_assets.append(
        {
            "id": str(uuid.uuid4()),
            "symbol": symbol,
            "name": data["name"],
            "image": data["image"],  # stripped ?query
            "is_fiat": False,
        }
    )
    existing_symbols.add(symbol)
    added += 1

# Save updated list
with open(output_file, "w") as f:
    json.dump(existing_assets, f, indent=2)

print(f"Added {added} new assets. Total: {len(existing_assets)} saved to {output_file}")

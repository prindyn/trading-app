import uuid
import json
import itertools
from pathlib import Path

# Resolve paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_FILE = BASE_DIR / "data" / "asset.json"
OUTPUT_FILE = BASE_DIR / "data" / "trade_pair.json"

# Load existing assets
with open(ASSETS_FILE, "r") as f:
    assets = json.load(f)

# Build symbol to id map
symbol_to_id = {a["symbol"].upper(): a["id"] for a in assets}
symbols = list(symbol_to_id.keys())

# Load existing trade pairs (if file exists)
existing_pairs = set()
existing_data = []

if OUTPUT_FILE.exists():
    with open(OUTPUT_FILE, "r") as f:
        try:
            existing_data = json.load(f)
            for pair in existing_data:
                key = (pair["base_symbol"], pair["quote_symbol"])
                existing_pairs.add(key)
        except:
            ...
# Generate new unique (base, quote) combinations
new_pairs = []
for base, quote in itertools.permutations(symbols, 2):
    key = (base, quote)
    if key in existing_pairs:
        continue
    new_pairs.append(
        {
            "id": str(uuid.uuid4()),
            "base_symbol": base,
            "base_asset_id": symbol_to_id[base],
            "quote_symbol": quote,
            "quote_asset_id": symbol_to_id[quote],
        }
    )
    existing_pairs.add(key)

# Append new pairs to existing and save
combined = existing_data + new_pairs
with open(OUTPUT_FILE, "w") as f:
    json.dump(combined, f, indent=2)

print(f"Added {len(new_pairs)} new trading pairs to {OUTPUT_FILE}")

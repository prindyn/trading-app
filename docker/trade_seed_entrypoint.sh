#!/bin/bash

set -e
set -o pipefail

echo "Seeding trade service DB..."

docker compose run --rm \
  --entrypoint "python -m seed.seed_all" \
  trade

echo "Trade DB seeding complete!"

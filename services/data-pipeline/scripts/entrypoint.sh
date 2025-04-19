#!/bin/bash

echo "Starting data pipeline service..."

if [ "$CRON_ENABLED" = "true" ]; then
  echo "Starting cron..."
  service cron start
fi

# Launch the async pipeline execution loop
exec python -m app.main

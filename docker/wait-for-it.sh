#!/usr/bin/env bash

HOST="$1"
PORT="$2"
shift 2

TIMEOUT=60  # You can bump this to 90 if needed

echo "Waiting for $HOST:$PORT for up to $TIMEOUT seconds..."

for i in $(seq $TIMEOUT); do
  if nc -z "$HOST" "$PORT"; then
    echo "$HOST:$PORT is available!"
    exec "$@"
    exit 0
  fi
  echo "[$i] Waiting..."
  sleep 1
done

echo "Timeout waiting for $HOST:$PORT"
exit 1

#!/usr/bin/env bash
#wait-for-it.sh - Wait for a host and TCP port to be available

set -e

HOST="$1"
PORT="$2"
shift 2
TIMEOUT=30

echo "Waiting for $HOST:$PORT..."

for i in $(seq $TIMEOUT); do
    if nc -z "$HOST" "$PORT"; then
        echo "$HOST:$PORT is available!"
        exec "$@"
        exit 0
    fi
    echo "Waiting... ($i/$TIMEOUT)"
    sleep 1
done

echo "Timeout after $TIMEOUT seconds waiting for $HOST:$PORT"
exit 1
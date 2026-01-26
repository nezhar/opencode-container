#!/bin/sh

set -e

TARGET_API_URL="${TARGET_API_URL:-}"
PROXY_PORT="${PROXY_PORT:-8080}"
PROXY_MODE="${PROXY_MODE:-reverse}"

if [ "$PROXY_MODE" = "reverse" ]; then
    if [ -z "$TARGET_API_URL" ]; then
        echo "TARGET_API_URL is required in reverse mode (e.g. https://api.openai.com)" >&2
        exit 1
    fi
    MODE_ARG="reverse:${TARGET_API_URL}"
else
    MODE_ARG="regular"
fi

exec mitmdump \
    --set "confdir=/proxy/certs" \
    -s "/proxy/proxy_script.py" \
    --listen-host "0.0.0.0" \
    --listen-port "$PROXY_PORT" \
    --mode "$MODE_ARG" \
    --ssl-insecure

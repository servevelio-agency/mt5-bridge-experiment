#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8000}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" -m bridge.probe &
PROBE_PID=$!
trap 'kill "$PROBE_PID" 2>/dev/null || true' EXIT

for _ in $(seq 1 20); do
  if curl -fsS "http://127.0.0.1:${PORT}/health" >/tmp/mt5-probe-response.json 2>/dev/null; then
    cat /tmp/mt5-probe-response.json
    exit 0
  fi
  sleep 0.5
done

cat /tmp/mt5-probe-response.json 2>/dev/null || echo "Probe did not become healthy in time" >&2
exit 1

#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${MT5_TERMINAL_PATH:-}" ]]; then
  echo "MT5_TERMINAL_PATH is required for the experiment" >&2
  exit 1
fi

if [[ ! -f "$MT5_TERMINAL_PATH" ]]; then
  echo "MT5 terminal not found at: $MT5_TERMINAL_PATH" >&2
  exit 1
fi

if command -v Xvfb >/dev/null 2>&1; then
  Xvfb "${DISPLAY:-:99}" -screen 0 1280x800x24 >/tmp/xvfb.log 2>&1 &
fi

wine "$MT5_TERMINAL_PATH" /portable >/tmp/mt5.log 2>&1 &
exec python3 -m bridge.health

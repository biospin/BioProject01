#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

PORT="${PORT:-8765}"
TOKEN="${BIOP01_DASHBOARD_TOKEN:-}"

if [[ -z "$TOKEN" ]]; then
  TOKEN="$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(18))
PY
)"
  export BIOP01_DASHBOARD_TOKEN="$TOKEN"
fi

echo "BioProject01 paper dashboard"
echo "Token: $TOKEN"
echo
echo "Local URL:"
echo "  http://127.0.0.1:$PORT"
echo
echo "LAN URL candidates:"
if command -v ipconfig >/dev/null 2>&1; then
  for iface in en0 en1; do
    ip="$(ipconfig getifaddr "$iface" 2>/dev/null || true)"
    if [[ -n "$ip" ]]; then
      echo "  http://$ip:$PORT"
    fi
  done
fi
if command -v ifconfig >/dev/null 2>&1; then
  ifconfig | awk '/inet / && $2 != "127.0.0.1" { print "  http://"$2":'"$PORT"'" }'
fi
echo
echo "Teammates should enter the token in the Team token field."
echo

exec python3 web/app.py --host 0.0.0.0 --port "$PORT" --token "$TOKEN"

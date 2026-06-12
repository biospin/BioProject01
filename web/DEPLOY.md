# Team Deployment

This dashboard is designed for small-team local sharing on the same network.

## Where To Check The Harness

```text
web/
  app.py
  index.html
  static/app.css
  static/app.js
  scripts/share_dashboard.sh

artifacts/
  README.md
  web-runs/
```

The original paper-analysis harness still lives in:

```text
AGENTS.md
skills/
analysis/
```

## Option 1. Each Teammate Runs Locally

Recommended for normal use.

```bash
git pull
cd /Users/kkkim/projects/autobiox/BioProject01
python3 web/app.py --port 8765
```

Open:

```text
http://127.0.0.1:8765
```

## Option 2. One Person Hosts On LAN

Use this for study sessions.

```bash
cd /Users/kkkim/projects/autobiox/BioProject01
BIOP01_DASHBOARD_TOKEN='team-token-here' python3 web/app.py --host 0.0.0.0 --port 8765
```

Find your LAN IP:

```bash
ipconfig getifaddr en0
```

Share:

```text
http://<lan-ip>:8765
```

Teammates enter `team-token-here` in the `Team token` field.

## Convenience Script

```bash
./web/scripts/share_dashboard.sh
```

The script starts the dashboard on `0.0.0.0:8765` and prints candidate LAN URLs.

## Security Boundary

The dashboard can read files inside this repository and run helper scripts for index rebuild
and HTML rendering. Do not expose it to the public internet. Use token mode for team sharing.

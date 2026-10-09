#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

export PORT="${PORT:-8080}"

python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt

exec .venv/bin/python app/app.py

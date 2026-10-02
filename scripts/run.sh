#!/usr/bin/env bash
set -euo pipefail

export PORT="${PORT:-8080}"

python3 app/app.py

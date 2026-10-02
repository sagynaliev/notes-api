#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH=. pytest -q

echo "TESTS: 5/5"

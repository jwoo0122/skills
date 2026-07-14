#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

PYTHONDONTWRITEBYTECODE=1 python3 "$ROOT/tests/test_package.py"
PYTHONDONTWRITEBYTECODE=1 python3 "$ROOT/tests/test_adr.py"

printf '%s\n' 'all checks: ok'

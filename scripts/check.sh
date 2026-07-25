#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON=$(
    CDPATH= cd -- "$ROOT" && \
        "$ROOT/skills/maintain-architecture-decisions/scripts/adr" --print-python
)

"$ROOT/skills/maintain-architecture-decisions/scripts/adr" validate --root "$ROOT"
"$ROOT/skills/maintain-architecture-decisions/scripts/adr" check --root "$ROOT"

PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$ROOT/tests/test_package.py"
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$ROOT/tests/test_adr.py"

printf '%s\n' 'all checks: ok'

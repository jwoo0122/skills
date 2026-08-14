#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root"
python=$(skills/maintain-architecture-decisions/scripts/adr --print-python --root .)

skills/maintain-architecture-decisions/scripts/adr check --root .
PYTHONDONTWRITEBYTECODE=1 "$python" -m unittest discover -s tests -p 'test_*.py'

before=$(sha256sum adr/index.yaml | cut -d' ' -f1)
skills/maintain-architecture-decisions/scripts/adr reindex --root .
after=$(sha256sum adr/index.yaml | cut -d' ' -f1)
[ "$before" = "$after" ] || {
  echo "reindex is not idempotent" >&2
  exit 1
}

echo "all checks: ok"

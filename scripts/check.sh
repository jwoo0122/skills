#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root"
python=$(scripts/adr --print-python --root .)

scripts/adr check --root .
PYTHONDONTWRITEBYTECODE=1 "$python" -m unittest discover -s tests -p 'test_*.py'

before=$(sha256sum adr/index.yaml | cut -d' ' -f1)
scripts/adr reindex --root .
after=$(sha256sum adr/index.yaml | cut -d' ' -f1)
[ "$before" = "$after" ] || {
  echo "reindex is not idempotent" >&2
  exit 1
}

echo "all checks: ok"

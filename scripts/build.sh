#!/usr/bin/env bash
# Build superagency.skill deterministically.
#
# zip embeds file mtimes, so a naive rebuild produces different bytes on every
# run even when nothing changed — which would make CI commit a phantom change
# on every push, and each bot push would retrigger the build. Normalizing
# timestamps and sorting the file list makes identical content produce an
# identical archive, so "did this actually change?" is just a byte comparison.
set -euo pipefail

cd "$(dirname "$0")/.."
OUT="$(pwd)/${1:-superagency.skill}"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cp -R superagency "$TMP/superagency"
find "$TMP/superagency" -name '.DS_Store' -delete
find "$TMP/superagency" -name '__pycache__' -type d -prune -exec rm -rf {} +
# 1980-01-01 is the earliest timestamp the zip format can represent.
find "$TMP/superagency" -exec touch -t 198001010000 {} +

rm -f "$OUT"
( cd "$TMP" && find superagency | sort | zip -qX "$OUT" -@ )

# Claude.ai rejects an archive whose paths don't start with superagency/
if unzip -Z1 "$OUT" | grep -qv '^superagency/'; then
  echo "error: archive contains paths outside superagency/" >&2
  unzip -Z1 "$OUT" | grep -v '^superagency/' >&2
  exit 1
fi

echo "built $(basename "$OUT") — $(unzip -Z1 "$OUT" | wc -l | tr -d ' ') entries, $(du -h "$OUT" | cut -f1 | tr -d ' ')"

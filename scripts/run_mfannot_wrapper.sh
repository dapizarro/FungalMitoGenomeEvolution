#!/usr/bin/env bash
set -euo pipefail
FASTA="$1"
OUT="$2"
CMD="${3:-mfannot}"
mkdir -p "$(dirname "$OUT")"
$CMD "$FASTA" > "$OUT"

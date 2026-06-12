#!/usr/bin/env bash
set -euo pipefail

# Build per-gene AA alignments and a concatenated IQ-TREE phylogeny.
# Expected input: one FASTA per gene in results/genes/cds_aa/{gene}.faa
# You can generate these from CDS after manual curation/translation.

GENE_DIR=${1:-results/genes/cds_aa}
ALN_DIR=${2:-results/alignments/per_gene}
TRIM_DIR=${3:-results/alignments/trimmed}
CONCAT_DIR=${4:-results/alignments/concat}
TREE_DIR=${5:-results/phylogeny}
THREADS=${THREADS:-AUTO}

mkdir -p "$ALN_DIR" "$TRIM_DIR" "$CONCAT_DIR" "$TREE_DIR"

for faa in "$GENE_DIR"/*.faa; do
  [ -e "$faa" ] || continue
  gene=$(basename "$faa" .faa)
  mafft --auto "$faa" > "$ALN_DIR/${gene}.aln.faa"
  trimal -in "$ALN_DIR/${gene}.aln.faa" -out "$TRIM_DIR/${gene}.trim.faa" -automated1
 done

python scripts/concat_alignments.py --indir "$TRIM_DIR" --output "$CONCAT_DIR/supermatrix.faa" --partitions "$CONCAT_DIR/partitions.txt"

iqtree2 -s "$CONCAT_DIR/supermatrix.faa" -p "$CONCAT_DIR/partitions.txt" -m MFP+MERGE -B 1000 --alrt 1000 -T "$THREADS" -pre "$TREE_DIR/mt_cds_supermatrix"

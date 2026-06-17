# mitogenome-fasta-evo-pipeline

Reproducible end-to-end pipeline for comparative mitochondrial genome analyses starting from raw mitochondrial genome FASTA files.

The pipeline is designed for fungal/lichenized fungal mitogenomes, but the structure is generic enough to be adapted to other eukaryotic mitochondrial datasets.

## What it does

Starting from mitochondrial genome FASTA files, the workflow can:

1. standardize input FASTA names and sample identifiers;
2. compute basic assembly/genome metrics;
3. annotate mitochondrial genomes using MFannot and/or MITOS2;
4. parse annotation outputs into unified feature tables;
5. build a consensus annotation table across tools;
6. extract CDS, rRNA, tRNA and optionally intron/intergenic features;
7. build gene presence/absence matrices;
8. translate and align protein-coding genes;
9. trim alignments and build concatenated supermatrices;
10. infer maximum-likelihood phylogenies with IQ-TREE2;
11. merge mitogenome traits with ecological metadata;
12. run exploratory statistics, GLMs/GLMMs, PCA, PERMANOVA and phylogenetic models such as PGLS.

## Repository layout

```text
mitogenome-fasta-evo-pipeline/
├── config/
│   └── config.yaml
├── data/
│   ├── raw/
│   │   └── mitogenomes/          # input FASTA files, one genome per file
│   └── metadata/
│       └── ecology.tsv           # optional ecological metadata
├── docs/
│   ├── input_format.md
│   └── methodology.md
├── envs/
│   └── mitogenomes.yml
├── results/
│   ├── annotation/
│   ├── features/
│   ├── genes/
│   ├── alignments/
│   ├── phylogeny/
│   ├── stats/
│   ├── figures/
│   └── tables/
├── scripts/
├── workflow/
│   ├── Snakefile
│   └── rules/
├── Makefile
└── README.md
```

## Input

Put mitochondrial genome FASTA files here:

```bash
data/raw/mitogenomes/
```

Recommended naming:

```text
Sample_001.fasta
Sample_002.fasta
Species_name_strain.fna
```

Each file should ideally contain one complete or draft mitochondrial genome. Multi-contig FASTA files are accepted.

Optional ecological metadata:

```bash
data/metadata/ecology.tsv
```

Minimum required column:

```text
sample_id
```

Example:

```text
sample_id	species	family	lifestyle	substrate	climate_zone	latitude	longitude
Sample_001	Evernia_prunastri	Parmeliaceae	lichenized	bark	temperate	40.1	-3.7
```

The `sample_id` must match the FASTA basename after removing extensions `.fa`, `.fna`, `.fasta`.

## Installation

Using mamba:

```bash
mamba env create -f envs/mitogenomes.yml
mamba activate mitogenomes
```

Some annotation tools, especially MFannot, are often easier to run through a container. The workflow provides placeholders for both direct execution and container-based execution.

## Run full workflow

Dry run:

```bash
snakemake -s workflow/Snakefile --configfile config/config.yaml -n
```

Run locally:

```bash
snakemake -s workflow/Snakefile --configfile config/config.yaml --cores 12
```

Run via Makefile:

```bash
make dryrun
make run CORES=12
```

## Main output tables

| File | Description |
|---|---|
| `results/tables/genome_metrics.tsv` | Genome size, GC, N content, contig number |
| `results/tables/feature_table.tsv` | Unified long-format annotation table |
| `results/tables/gene_presence_absence.tsv` | Matrix of mitochondrial gene presence/absence |
| `results/tables/gene_lengths.tsv` | Per-sample per-gene lengths |
| `results/tables/mitogenome_traits.tsv` | Combined mitogenome traits |
| `results/tables/mitogenome_traits_with_ecology.tsv` | Mitogenome traits merged with ecology |
| `results/stats/statistical_models.tsv` | Non-phylogenetic model summary |
| `results/stats/pgls_models.tsv` | Phylogenetic model summary |

## Recommended workflow logic

1. Run annotation with MFannot/MITOS2.
2. Inspect consensus annotations manually for problematic genes.
3. Extract canonical mitochondrial CDS.
4. Build per-gene alignments.
5. Filter poor alignments and genes with low occupancy.
6. Infer concatenated ML tree.
7. Use that tree in PGLS/phylogenetic signal analyses.
8. Relate mitogenome traits to ecological metadata.

## Status

🚧 Work in progress.

This repository contains an actively developed pipeline for comparative mitochondrial genome analyses. Methods, scripts, and outputs may evolve as development continues.

A manuscript describing the pipeline is not currently available.

If you use this repository, please cite:

> Pizarro D. (2026). mitogenome-fasta-evo-pipeline. https://doi.org/10.5281/zenodo.20700778

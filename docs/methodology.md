# Methodological outline

## 1. Input standardization

The pipeline starts from raw mitochondrial genome FASTA files. A sample table is generated automatically from file names.

## 2. Genome metrics

For each genome, the pipeline calculates genome size, number of contigs, GC percentage, N content and N fraction.

## 3. Annotation

The default annotation route is MFannot, with optional MITOS2 support. The command is configured in `config/config.yaml`. Because MFannot installations differ, the wrapper is intentionally simple and can be replaced by a Docker/Singularity command.

## 4. Feature harmonization

GFF outputs are parsed into a unified long-format table with one row per feature and coordinates, strand, feature type, gene name, product and source tool.

## 5. Comparative tables

The workflow creates:

- feature table;
- gene presence/absence matrix;
- per-gene length matrix;
- genome-level mitogenome trait table;
- mitogenome trait table merged with ecological metadata.

## 6. Phylogenetic reconstruction

After CDS curation and translation, per-gene AA FASTA files can be aligned with MAFFT, trimmed with trimAl and concatenated. IQ-TREE2 is used with partition merging and ultrafast bootstrap/aLRT support.

## 7. Statistical analyses

The Python statistical module fits simple OLS models for mitogenome traits against ecological predictors. The R module fits PGLS models using a mitochondrial phylogeny, allowing ecological effects to be tested while accounting for shared ancestry.

## 8. Recommended analyses for publication

Recommended response variables:

- mitochondrial genome size;
- GC percentage;
- CDS count;
- tRNA/rRNA count;
- intron count;
- intergenic fraction;
- gene presence/absence distances;
- gene order rearrangements if coordinates are sufficiently complete.

Recommended ecological predictors:

- lifestyle;
- substrate;
- photobiont class, if available;
- climate zone;
- host family/order;
- biome or macroclimatic region.

Recommended phylogenetic analyses:

- concatenated ML tree from conserved mitochondrial proteins;
- single-gene trees for conflict inspection;
- phylogenetic signal of mitogenome traits;
- PGLS models for ecology-trait associations;
- ancestral state reconstruction for selected traits.

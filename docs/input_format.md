# Input format

## Mitogenome FASTA files

Place one mitochondrial genome per file in:

```bash
data/raw/mitogenomes/
```

Accepted extensions: `.fa`, `.fna`, `.fasta`.

The sample identifier is the filename without extension. For example:

```text
data/raw/mitogenomes/ERR10794125.fasta -> sample_id = ERR10794125
```

## Ecology table

Optional file:

```bash
data/metadata/ecology.tsv
```

Required column:

```text
sample_id
```

Recommended columns:

```text
sample_id species family order lifestyle substrate climate_zone latitude longitude source
```

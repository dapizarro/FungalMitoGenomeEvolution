#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly=TRUE)
table_file <- args[1]
tree_file <- args[2]
out_file <- args[3]

suppressPackageStartupMessages({library(readr); library(dplyr); library(ape); library(caper); library(broom)})

dat <- read_tsv(table_file, show_col_types=FALSE)
responses <- c('genome_size_bp','gc_percent','cds_count','trna_count','rrna_count','intron_count','intergenic_fraction')
predictors <- c('lifestyle','substrate','climate_zone')
rows <- list()

if (!file.exists(tree_file)) {
  write_tsv(tibble(note='No phylogenetic tree found. Run IQ-TREE first or set statistics.phylogenetic_tree in config.yaml.'), out_file)
  quit(save='no')
}

tree <- read.tree(tree_file)
if (!'sample_id' %in% names(dat)) stop('sample_id column required')
rownames(dat) <- dat$sample_id
common <- intersect(tree$tip.label, dat$sample_id)
tree <- drop.tip(tree, setdiff(tree$tip.label, common))
dat <- dat[common, , drop=FALSE]

for (y in intersect(responses, names(dat))) {
  for (x in intersect(predictors, names(dat))) {
    sub <- dat[, c('sample_id', y, x)] |> na.omit()
    if (nrow(sub) < 6 || length(unique(sub[[x]])) < 2) next
    rownames(sub) <- sub$sample_id
    tr <- drop.tip(tree, setdiff(tree$tip.label, sub$sample_id))
    comp <- comparative.data(tr, sub, names.col='sample_id', vcv=TRUE, warn.dropped=FALSE)
    form <- as.formula(paste(y, '~', x))
    fit <- try(pgls(form, data=comp, lambda='ML'), silent=TRUE)
    if (!inherits(fit, 'try-error')) {
      tt <- broom::tidy(fit)
      tt$response <- y; tt$predictor <- x; tt$n <- nrow(sub); tt$lambda <- fit$param['lambda']
      rows[[length(rows)+1]] <- tt
    }
  }
}

res <- if (length(rows)) bind_rows(rows) else tibble(note='No valid PGLS models fitted')
write_tsv(res, out_file)

CORES ?= 8
CONFIG ?= config/config.yaml

.PHONY: dryrun run unlock clean

dryrun:
	snakemake -s workflow/Snakefile --configfile $(CONFIG) -n

run:
	snakemake -s workflow/Snakefile --configfile $(CONFIG) --cores $(CORES)

unlock:
	snakemake -s workflow/Snakefile --configfile $(CONFIG) --unlock

clean:
	rm -rf results/*

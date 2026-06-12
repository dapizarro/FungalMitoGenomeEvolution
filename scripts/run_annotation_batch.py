#!/usr/bin/env python3
import argparse, subprocess
from pathlib import Path
import pandas as pd

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--samples',required=True); ap.add_argument('--outdir',required=True)
    ap.add_argument('--tool',choices=['mfannot','mitos'],required=True); ap.add_argument('--command',required=True)
    a=ap.parse_args(); out=Path(a.outdir); out.mkdir(parents=True,exist_ok=True)
    samples=pd.read_csv(a.samples,sep='\t')
    for _,r in samples.iterrows():
        sample=r.sample_id; fasta=r.fasta
        gff=out/f'{sample}.gff3'
        if gff.exists() and gff.stat().st_size>0: continue
        # Generic wrapper. For real MFannot installations, edit this command if your executable syntax differs.
        cmd=f"{a.command} {fasta} > {gff}"
        print(f'Running {a.tool}: {sample}')
        try:
            subprocess.run(cmd,shell=True,check=True)
        except subprocess.CalledProcessError:
            gff.write_text('##gff-version 3\n# Annotation failed or command not configured. Replace command in config/config.yaml.\n')
            print(f'WARNING: annotation failed for {sample}; placeholder GFF written.')
if __name__=='__main__': main()

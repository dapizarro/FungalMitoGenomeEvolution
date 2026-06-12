#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd
from Bio import SeqIO

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--samples'); ap.add_argument('--features'); ap.add_argument('--outdir'); a=ap.parse_args()
    out=Path(a.outdir); (out/'cds').mkdir(parents=True,exist_ok=True); (out/'all_features').mkdir(parents=True,exist_ok=True)
    samples=pd.read_csv(a.samples,sep='\t').set_index('sample_id'); feat=pd.read_csv(a.features,sep='\t')
    for sample,sub in feat.groupby('sample_id'):
        if sample not in samples.index: continue
        recs=SeqIO.to_dict(SeqIO.parse(samples.loc[sample,'fasta'],'fasta'))
        for _,r in sub.iterrows():
            if r.seqid not in recs: continue
            seq=recs[r.seqid].seq[int(r.start)-1:int(r.end)]
            if r.strand=='-': seq=seq.reverse_complement()
            fname=out/'all_features'/f'{sample}__{r.gene}__{r.feature_type}.fasta'
            with open(fname,'w') as h: h.write(f'>{sample}|{r.gene}|{r.feature_type}\n{seq}\n')
if __name__=='__main__': main()

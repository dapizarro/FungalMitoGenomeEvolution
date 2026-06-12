#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd
from Bio import SeqIO

def gc(seq):
    s=str(seq).upper(); atgc=sum(s.count(x) for x in 'ATGC')
    return 100*(s.count('G')+s.count('C'))/atgc if atgc else 0

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--samples'); ap.add_argument('--output'); a=ap.parse_args()
    smp=pd.read_csv(a.samples,sep='\t'); rows=[]
    for _,r in smp.iterrows():
        recs=list(SeqIO.parse(r.fasta,'fasta'))
        total=sum(len(x.seq) for x in recs); n=sum(str(x.seq).upper().count('N') for x in recs)
        joined=''.join(str(x.seq) for x in recs)
        rows.append({'sample_id':r.sample_id,'contig_count':len(recs),'genome_size_bp':total,'gc_percent':gc(joined),'n_count':n,'n_fraction':n/total if total else 0})
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(a.output,sep='\t',index=False)
if __name__=='__main__': main()

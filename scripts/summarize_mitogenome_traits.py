#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd

def count_type(df, pattern):
    return df[df.feature_type.str.lower().str.contains(pattern,na=False)].groupby('sample_id').size()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--metrics'); ap.add_argument('--features'); ap.add_argument('--presence'); ap.add_argument('--output'); a=ap.parse_args()
    m=pd.read_csv(a.metrics,sep='\t'); f=pd.read_csv(a.features,sep='\t')
    out=m.set_index('sample_id')
    if not f.empty:
        for name,pat in [('cds_count','cds'),('trna_count','trna'),('rrna_count','rrna|rRNA'),('intron_count','intron')]:
            out[name]=count_type(f,pat)
        gene_len=f.groupby('sample_id')['length_bp'].sum()
        out['annotated_bp']=gene_len
        out['intergenic_bp']=(out['genome_size_bp']-out['annotated_bp']).clip(lower=0)
        out['intergenic_fraction']=out['intergenic_bp']/out['genome_size_bp']
    out=out.fillna(0).reset_index()
    Path(a.output).parent.mkdir(parents=True,exist_ok=True); out.to_csv(a.output,sep='\t',index=False)
if __name__=='__main__': main()

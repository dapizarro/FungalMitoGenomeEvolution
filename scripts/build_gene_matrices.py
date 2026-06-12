#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--features'); ap.add_argument('--presence'); ap.add_argument('--lengths'); a=ap.parse_args()
    df=pd.read_csv(a.features,sep='\t')
    if df.empty:
        pres=pd.DataFrame(); lens=pd.DataFrame()
    else:
        df=df[df['feature_type'].str.lower().isin(['gene','cds','trna','rrna','exon']) | df['gene'].notna()]
        pres=pd.crosstab(df.sample_id, df.gene).clip(upper=1).reset_index()
        lens=df.pivot_table(index='sample_id',columns='gene',values='length_bp',aggfunc='max').reset_index()
    Path(a.presence).parent.mkdir(parents=True,exist_ok=True)
    pres.to_csv(a.presence,sep='\t',index=False); lens.to_csv(a.lengths,sep='\t',index=False)
if __name__=='__main__': main()

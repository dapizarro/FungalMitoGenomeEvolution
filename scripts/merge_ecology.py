#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--traits'); ap.add_argument('--ecology'); ap.add_argument('--output'); a=ap.parse_args()
    t=pd.read_csv(a.traits,sep='\t')
    if Path(a.ecology).exists() and Path(a.ecology).stat().st_size>0:
        e=pd.read_csv(a.ecology,sep='\t')
        if 'sample_id' not in e.columns: raise SystemExit('ecology.tsv must contain sample_id')
        out=t.merge(e,on='sample_id',how='left')
    else:
        out=t
    Path(a.output).parent.mkdir(parents=True,exist_ok=True); out.to_csv(a.output,sep='\t',index=False)
if __name__=='__main__': main()

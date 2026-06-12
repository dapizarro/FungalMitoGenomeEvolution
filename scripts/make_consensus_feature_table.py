#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--features'); ap.add_argument('--output'); a=ap.parse_args()
    df=pd.read_csv(a.features,sep='\t') if Path(a.features).stat().st_size else pd.DataFrame()
    if df.empty:
        out=pd.DataFrame(columns=['sample_id','gene','feature_type','seqid','start','end','strand','length_bp','support_tools'])
    else:
        key=['sample_id','gene','feature_type','seqid','start','end','strand']
        out=df.groupby(key,dropna=False).agg(length_bp=('length_bp','max'),support_tools=('tool',lambda x: ','.join(sorted(set(x))))).reset_index()
    Path(a.output).parent.mkdir(parents=True,exist_ok=True); out.to_csv(a.output,sep='\t',index=False)
if __name__=='__main__': main()

#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd

EXTS={'.fa','.fna','.fasta'}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input-dir',required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args()
    rows=[]
    for p in sorted(Path(a.input_dir).iterdir()):
        if p.suffix.lower() in EXTS:
            rows.append({'sample_id':p.stem,'fasta':str(p)})
    if not rows:
        raise SystemExit(f'No FASTA files found in {a.input_dir}')
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(a.output,sep='\t',index=False)
if __name__=='__main__': main()

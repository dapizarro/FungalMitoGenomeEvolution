#!/usr/bin/env python3
import argparse, re
from pathlib import Path
import pandas as pd

def attrs(s):
    d={}
    for part in s.split(';'):
        if '=' in part:
            k,v=part.split('=',1); d[k]=v
        elif ' ' in part:
            k,v=part.split(' ',1); d[k]=v.strip('"')
    return d

def norm_gene(d,ftype):
    for k in ['gene','Name','product','ID','locus_tag']:
        if k in d and d[k]: return re.sub(r'[^A-Za-z0-9_.-]+','_',d[k]).strip('_')
    return ftype

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--tool'); ap.add_argument('--gff-dir'); ap.add_argument('--output'); a=ap.parse_args()
    rows=[]
    for gff in sorted(Path(a.gff_dir).glob('*.gff*')):
        sample=gff.name.split('.')[0]
        for line in gff.read_text(errors='ignore').splitlines():
            if not line or line.startswith('#'): continue
            f=line.split('\t')
            if len(f)<9: continue
            seqid,source,ftype,start,end,score,strand,phase,att=f[:9]
            d=attrs(att); gene=norm_gene(d,ftype)
            rows.append({'sample_id':sample,'tool':a.tool,'seqid':seqid,'source':source,'feature_type':ftype,'start':int(start),'end':int(end),'strand':strand,'phase':phase,'gene':gene,'product':d.get('product',''),'attributes':att,'length_bp':abs(int(end)-int(start))+1})
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(a.output,sep='\t',index=False)
if __name__=='__main__': main()

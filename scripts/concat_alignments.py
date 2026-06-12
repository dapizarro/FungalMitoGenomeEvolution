#!/usr/bin/env python3
import argparse
from pathlib import Path
from Bio import SeqIO

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--indir'); ap.add_argument('--output'); ap.add_argument('--partitions'); a=ap.parse_args()
    files=sorted(Path(a.indir).glob('*.faa')) + sorted(Path(a.indir).glob('*.aln'))
    taxa=set(); data=[]
    for f in files:
        recs={r.id:str(r.seq) for r in SeqIO.parse(f,'fasta')}
        if recs:
            data.append((f.stem,recs,len(next(iter(recs.values()))))); taxa.update(recs)
    taxa=sorted(taxa); concat={t:'' for t in taxa}; parts=[]; pos=1
    for gene,recs,L in data:
        for t in taxa: concat[t]+=recs.get(t,'-'*L)
        parts.append(f'{gene} = {pos}-{pos+L-1}'); pos+=L
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    with open(a.output,'w') as h:
        for t,s in concat.items(): h.write(f'>{t}\n{s}\n')
    with open(a.partitions,'w') as h: h.write('\n'.join(parts)+'\n')
if __name__=='__main__': main()

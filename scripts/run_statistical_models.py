#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd
import statsmodels.formula.api as smf

RESPONSES=['genome_size_bp','gc_percent','cds_count','trna_count','rrna_count','intron_count','intergenic_fraction']
PREDICTORS=['lifestyle','substrate','climate_zone']

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--table'); ap.add_argument('--output'); a=ap.parse_args()
    df=pd.read_csv(a.table,sep='\t')
    rows=[]
    for y in RESPONSES:
        if y not in df.columns: continue
        preds=[p for p in PREDICTORS if p in df.columns and df[p].notna().sum()>2 and df[p].nunique()>1]
        for p in preds:
            sub=df[[y,p]].dropna()
            if len(sub)<6 or sub[p].nunique()<2: continue
            try:
                model=smf.ols(f'{y} ~ C({p})',data=sub).fit()
                rows.append({'response':y,'predictor':p,'n':len(sub),'r2':model.rsquared,'aic':model.aic,'p_model':model.f_pvalue})
            except Exception as e:
                rows.append({'response':y,'predictor':p,'n':len(sub),'error':str(e)})
    out=pd.DataFrame(rows)
    Path(a.output).parent.mkdir(parents=True,exist_ok=True); out.to_csv(a.output,sep='\t',index=False)
if __name__=='__main__': main()

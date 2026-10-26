import numpy as np, pandas as pd, json, warnings; warnings.filterwarnings('ignore')
import statsmodels.api as sm
import frontlib as L
from fronts2 import features, df, C
Y=L.Y
typ=L.typ
out={}
for res in ['r3.0','r6.0','r12.0']:
    F,_=features(C[res].values, df.bal); F['type']=F.apply(typ,axis=1)
    # absolute growth (no offset)
    ab=[]
    for _,r in F.iterrows():
        n=np.array([r[f'n{y}'] for y in Y],float); m=sm.GLM(n, sm.add_constant(np.arange(len(Y))), family=sm.families.Poisson()).fit(scale='X2'); ab.append((np.exp(m.params[1])-1)*100)
    F['g_abs']=ab; out[res]=F
F=out['r6.0']; L.df['micro']=C['r6.0'].values; F['terms']=F.cluster.map(L.ctfidf('micro',F.cluster.tolist()))
F.to_pickle('fronts_final.pkl')
order=['Emergent','Growing','Stable','Peaked','Declining']
def summ(F):
    g=F.groupby('type'); s=g.agg(fronts=('cluster','size'),items=('size','sum'),g_share_med=('g_share','median'),g_abs_med=('g_abs','median'))
    for k,col in [('core_%','core'),('adj_%','adj'),('periph_%','periph'),('covid_%','covid'),('genai_%','genai'),('ai_%','ai')]:
        s[k]=g.apply(lambda x:(x['size']*x[col]).sum()/x['size'].sum())
    s['share_first']=g[f's{Y[0]}'].sum(); s['share2020']=g.s2020.sum(); s['share2025']=g.s2025.sum(); return s.reindex(order).round(2)
S={r:summ(Fr) for r,Fr in out.items()}
for r in S: print(r); print(S[r].to_string())
base=pd.Series(out['r6.0'].set_index('cluster').type).reindex(C['r6.0'].values).values; ag={}
for r in ['r3.0','r12.0']:
    it=pd.Series(out[r].set_index('cluster').type).reindex(C[r].values).values; m=df.bal.values&pd.notna(base)&pd.notna(it); ag[r]=float((base[m]==it[m]).mean())
print('agreement',ag)
# where do core items go: share of core items in each type (2020 vs 2025)
d=df[df.bal].copy(); d['type']=base[df.bal.values]
ct=d.groupby(['tier','Year','type']).size().unstack().fillna(0); ct=ct.div(ct.sum(1),axis=0)*100
print(ct.loc['C'].round(1)); print(ct.loc['P'].round(1))
# how many declining fronts decline in absolute terms
dec=F[F.type=='Declining']; print('declining fronts', len(dec), 'abs decline sig?', (dec.g_abs<0).sum())
# COVID / GenAI dictionary concentration: share of matched items in top-3 fronts (balanced)
conc={}
for k in ['COVID-19','GenAI']:
    x=d[d[k]].groupby(base[df.bal.values][d[k].values] if False else d.loc[d[k],'micro'] if 'micro' in d else None)
dd=df[df.bal].copy(); dd['micro']=C['r6.0'].values[df.bal.values]
for k in ['COVID-19','GenAI','AI (broad)']:
    v=dd[dd[k]].micro.value_counts(normalize=True); conc[k]=dict(top3=float(v.head(3).sum()*100), top_fronts=v.head(3).index.tolist(), n_fronts_50pct=int((v.cumsum()<0.5).sum()+1))
print(conc)
json.dump({'agreement':ag,'summ':{r:S[r].reset_index().to_dict('records') for r in S},'tiertype_C':ct.loc['C'].round(2).reset_index().to_dict('records'),'tiertype_P':ct.loc['P'].round(2).reset_index().to_dict('records'),'conc':conc},open('fronts_meta.json','w'))
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',60)
for t in ['Peaked','Declining']:
    print('==',t); print(F[F.type==t].sort_values('size',ascending=False)[['cluster','size','s2017','s2020','s2025','g_share','g_abs','peak_year','core','covid','terms']].round(1).to_string())

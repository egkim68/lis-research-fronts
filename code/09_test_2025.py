import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
import statsmodels.api as sm, statsmodels.formula.api as smf
df=pd.read_pickle('clean.pkl'); CL=pd.read_pickle('clusters_scan.pkl'); df['front']=CL['r6.0'].values
F=pd.read_pickle('fronts_final.pkl'); tmap=F.set_index('cluster').type
M=df.groupby(['jn','Year']).size().unstack(fill_value=0); bal=M.index[(M>0).all(axis=1)]
d=df[df.jn.isin(bal)].copy(); d['ft']=d.front.map(tmap).fillna('Unclassified'); d=d[d.ft!='Unclassified']
c=d.groupby(['jn','Year','ft']).size().unstack(fill_value=0).stack().rename('n').reset_index()
c['tier']=c.jn.map(df.groupby('jn').tier.first()); c['t']=c.Year-2016; c['b25']=(c.Year==2025).astype(int); c['g']=c.jn+'|'+c.ft
rows=[]
for T in ['C','P','All']:
    x=c if T=='All' else c[c.tier==T]; x=x[x.groupby('g').n.transform('sum')>0]
    m=smf.glm('n ~ C(g) + t:C(ft) + b25:C(ft) - 1', data=x, family=sm.families.Poisson()).fit(cov_type='cluster', cov_kwds={'groups':pd.factorize(x.jn)[0]})
    for a in ['Emergent','Growing','Stable','Peaked','Declining']:
        for term,lab in [(f't:C(ft)[{a}]','trend'),(f'b25:C(ft)[{a}]','break2025')]:
            b,se,p=m.params[term],m.bse[term],m.pvalues[term]
            rows.append(dict(tier=T,type=a,term=lab,pct=(np.exp(b)-1)*100,lo=(np.exp(b-1.96*se)-1)*100,hi=(np.exp(b+1.96*se)-1)*100,p=p,journals=x.jn.nunique()))
R=pd.DataFrame(rows).round(3); R.to_csv('its_type.csv',index=False)
print(R.pivot_table(index=['tier','type'],columns='term',values=['pct','p']).round(3))
# contribution of each type to 2024->2025 net change in core and all
for T in ['C','All']:
    x=d if T=='All' else d[d.tier=='C']; t=x.groupby(['Year','ft']).size().unstack()
    dd=t.loc[2025]-t.loc[2024]; print(T, dd.to_dict(), 'total', dd.sum())

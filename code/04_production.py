import pandas as pd, numpy as np, json
df = pd.read_pickle('clean.pkl'); Y = list(range(2016, 2026))
R = {}
T = df.groupby(['Year','tier']).size().unstack()[['C','A','P']]; T['All'] = T.sum(1)
R['tier_counts'] = T
R['tier_share'] = (T[['C','A','P']].div(T.All, axis=0)*100).round(1)
cagr = lambda a, b, n: ((b/a)**(1/n)-1)*100
print(T); print(R['tier_share'])
print('CAGR 16-25', {k: round(cagr(T.loc[2016,k], T.loc[2025,k], 9),2) for k in T}); print('CAGR 20-25', {k: round(cagr(T.loc[2020,k], T.loc[2025,k], 5),2) for k in T})
R['domain_counts'] = df.groupby(['Year','domain']).size().unstack().T
# journal-year matrix
M = df.groupby(['jn','Year']).size().unstack(fill_value=0).reindex(columns=Y, fill_value=0)
tier = df.groupby('jn').tier.first(); name = df.groupby('jn').jname.first()
act = (M>0)
R['active_journals'] = act.groupby(tier).sum().T.assign(All=act.sum())
R['mean_per_journal'] = (M.where(act).groupby(tier).mean().T).round(1)
R['median_per_journal'] = (M.where(act).groupby(tier).median().T)
# Balanced panel
bal = act.all(1)
B = M[bal].groupby(tier[bal]).sum().T; B['All']=B.sum(1)
R['balanced_panel'] = B; print('balanced journals', bal.sum(), bal.groupby(tier).sum().to_dict()); print(B)
print('Balanced CAGR 16-25', {k: round(cagr(B.loc[2016,k], B.loc[2025,k],9),2) for k in B})
# Growth decomposition year to year: incumbents (active both years), entrants, exits
rows=[]
for t0,t1 in zip(Y[:-1],Y[1:]):
    for tr in ['C','A','P','All']:
        m = M if tr=='All' else M[tier==tr]
        a0, a1 = m[t0]>0, m[t1]>0
        inc = (m.loc[a0&a1, t1]-m.loc[a0&a1, t0]).sum()
        ent = m.loc[~a0&a1, t1].sum(); ex = -m.loc[a0&~a1, t0].sum()
        rows.append(dict(period=f'{t0}-{t1}', tier=tr, total=m[t1].sum()-m[t0].sum(), incumbents=inc, entrants=ent, exits=ex))
R['decomp'] = pd.DataFrame(rows); print(R['decomp'][R['decomp'].tier=='All'])
# Concentration of growth 2024->2025 and 2020->2025
for a,b in [(2024,2025),(2016,2025),(2020,2025)]:
    d = (M[b]-M[a]).sort_values(ascending=False)
    tot = d.sum(); top = d.head(10)
    R[f'top_growth_{a}_{b}'] = pd.DataFrame({'journal':name[top.index], 'tier':tier[top.index], 'delta':top.values, 'share_of_net_growth_%':(top/tot*100).round(1).values})
    print(a,b,'net',tot); print(R[f'top_growth_{a}_{b}'])
# Concentration: HHI and Gini; share of top-10 journals
def gini(x):
    x=np.sort(x[x>0]); n=len(x); return (2*np.arange(1,n+1)-n-1)@x/(n*x.sum())
conc=[]
for y in Y:
    for tr in ['C','A','P','All']:
        x = (M[y] if tr=='All' else M.loc[tier==tr, y]).values.astype(float)
        s = x[x>0]/x.sum()
        conc.append(dict(Year=y, tier=tr, HHI=round((s**2).sum()*10000,1), Gini=round(gini(x),3), top10_share=round(np.sort(s)[::-1][:10].sum()*100,1), eff_journals=round(1/(s**2).sum(),1)))
R['concentration'] = pd.DataFrame(conc); print(R['concentration'][R['concentration'].tier.isin(['All','C'])])
# log decomposition: output growth = journals growth + productivity growth
lg = pd.DataFrame({'log_output':np.log(M.sum()), 'log_journals':np.log(act.sum())}); lg['log_per_journal']=lg.log_output-lg.log_journals
R['log_decomp'] = (lg - lg.loc[2016]).round(3); print(R['log_decomp'])
# Coverage-shock journals
R['coverage_shocks'] = M.loc[['library philosophy and practice','webology','information sciences letters','library and information service','discover computing']].rename(index=name)
# Without the three delisted titles, core trend
drop = ['library philosophy and practice','webology']
Tc = M[(tier=='C') & ~M.index.isin(drop)].sum(); R['core_excl_delisted'] = Tc; print('core excl delisted', Tc.to_dict())
# Team size by tier-year
R['authors_mean'] = df.groupby(['Year','tier']).nauth.mean().unstack().round(2)
R['M'] = M.assign(tier=tier, journal=name)
pd.to_pickle(R, 'R_prod.pkl')

import numpy as np, pandas as pd, scipy.sparse as sp, pickle, warnings; warnings.filterwarnings('ignore')
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.special import gammaln
import statsmodels.api as sm
import os
df = pd.read_pickle('clean.pkl').merge(pd.read_pickle('art_flags.pkl'), on='EID')
C = pd.read_pickle('clusters_scan.pkl'); df['macro']=C['r1.5'].values; df['micro']=C['r6.0'].values
X = sp.load_npz('X.npz'); terms=np.array(pickle.load(open('vec.pkl','rb')).get_feature_names_out())
Y=list(range(2016,2026)); Nt=df.groupby('Year').size().reindex(Y)
BASE=[2016,2017,2018,2019]; PEAK=[2020,2021,2022]   # pre-pandemic baseline; pandemic-era peak years
def typ(r, E=3, rise=1.15, fall=0.6, alpha=0.05):
    s=np.array([r[f's{y}'] for y in Y]); base=s[:len(BASE)].mean(); end=s[-2:].mean(); ip=Y[int(np.argmax(s))]
    if ip in PEAK and s.max()>=rise*base and s[-1]<=fall*s.max(): return 'Peaked'
    if end>=E*max(base,1e-6): return 'Emergent'
    if r.g_p<alpha and r.g_share>0: return 'Growing'
    if r.g_p<alpha and r.g_share<0: return 'Declining'
    return 'Stable'
def ctfidf(col, ids, top=8):
    out={}
    tot = np.asarray(X.sum(0)).ravel(); tot=tot/tot.sum()
    for c in ids:
        m=(df[col]==c).values; v=np.asarray(X[m].sum(0)).ravel(); v=v/v.sum()
        sc = v*np.log1p(v/(tot+1e-12)); out[c]=', '.join(terms[np.argsort(-sc)[:top]])
    return out
def burst(r, d, s=2.0, gamma=1.0):
    # Kleinberg (2003) two-state batched burst detection
    n=len(r); p0=r.sum()/d.sum(); p=[p0, min(0.9999,s*p0)]
    def cost(i,t): return -(gammaln(d[t]+1)-gammaln(r[t]+1)-gammaln(d[t]-r[t]+1)+r[t]*np.log(p[i])+(d[t]-r[t])*np.log(1-p[i]))
    tau=gamma*np.log(n); C=np.zeros((n,2)); B=np.zeros((n,2),int)
    C[0]=[cost(0,0), cost(1,0)+tau]
    for t in range(1,n):
        for j in range(2):
            opts=[C[t-1,i]+(tau if j>i else 0) for i in range(2)]; B[t,j]=int(np.argmin(opts)); C[t,j]=min(opts)+cost(j,t)
    st=[int(np.argmin(C[-1]))]
    for t in range(n-1,0,-1): st.append(B[t,st[-1]])
    st=st[::-1]; strength=sum(cost(0,t)-cost(1,t) for t in range(n) if st[t]==1)
    return st, strength

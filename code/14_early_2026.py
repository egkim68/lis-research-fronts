"""Preliminary 2026 check: assign 2026 records to the existing fronts and topics by 15-nearest-neighbour vote.
Usage (run in the pipeline working directory after steps 00-08): python 14_early_2026.py <Scopus CSV for 2026>"""
import sys, re, pickle, numpy as np, pandas as pd, scipy.sparse as sp
sys.path.insert(0,'.')
from journal_tiers import TIERS, norm
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
B=''
raw=pd.read_csv(sys.argv[1],dtype=str).drop_duplicates('EID')
print('raw',len(raw), raw.Year.value_counts().to_dict())
old=pd.read_pickle(B+'all.pkl'); print('overlap with 2020-25 EIDs', raw.EID.isin(old.EID).sum())
raw=raw[raw.Year=='2026'].copy()
raw['jn']=raw['Source title'].map(norm); miss=sorted(set(raw.jn)-set(TIERS)); print('unmapped',miss)
raw=raw[raw.jn.isin(TIERS)]
print(raw['Document Type'].value_counts().to_dict()); print(raw['Publication Stage'].value_counts().to_dict())
keep=['Article','Review','Conference paper','Data paper','Short survey']
d=raw[raw['Document Type'].isin(keep)].copy()
def clean_abs(a):
    if not isinstance(a,str) or a.startswith('[No abstract'): return ''
    a=re.split(r'\s©|\s\(C\)\s|Copyright ©',a)[0]
    a=re.sub(r'(\d+(st|nd|rd|th) )?Annual Meeting of the Association for Information Science.*$','',a)
    a=re.sub(r'This briefing is prepared by an independent writer[^.]*\.','',a)
    a=re.sub(r'The briefing saves busy executives[^.]*\.','',a)
    a=re.sub(r'(Purpose|Design/methodology/approach|Findings|Originality/value|Research limitations/implications|Practical implications|Social implications)\s*:',' ',a)
    a=re.sub(r'\[(Purpose/Significance|Method/Process|Results?/Conclusions?|Objective|Methods?|Results?|Conclusions?|Limitations?)\]',' ',a)
    return a
d['abs']=d.Abstract.map(clean_abs); d['kw']=d['Author Keywords'].fillna('')
d['text']=(d.Title.fillna('')+'. '+d['abs']+' '+d.kw.str.replace(';',' ')).str.lower()
d['tier']=d.jn.map(lambda j:TIERS[j][0]); d['Year']=2026
print('research items 2026',len(d), d.tier.value_counts().to_dict(), 'no abstract', round((d['abs']=='').mean(),3))
vec=pickle.load(open(B+'vec.pkl','rb')); X=sp.load_npz(B+'X.npz'); Z=np.load(B+'Z.npy')
svd=TruncatedSVD(n_components=256,random_state=7).fit(X)
Zr=normalize(svd.transform(X[:5000])); print('SVD reproduces Z: min row cosine', float((Zr*Z[:5000]).sum(1).min()))
Zn=normalize(svd.transform(vec.transform(d.text))).astype(np.float32)
np.save('Z26.npy',Zn); d.reset_index(drop=True).to_pickle('d26.pkl')
import gc; del X, Zr, svd, old, raw, Zn, d, vec; gc.collect()

Z=np.load(B+'Z.npy'); C=pd.read_pickle(B+'clusters_scan.pkl'); df=pd.read_pickle(B+'clean.pkl')
Z26=np.load('Z26.npy'); d=pd.read_pickle('d26.pkl')
K=15
def knn(Q, exclude_self_offset=None):
    I=np.zeros((len(Q),K),np.int64); S=np.zeros((len(Q),K),np.float32)
    for a in range(0,len(Q),500):
        sim=Q[a:a+500]@Z.T
        if exclude_self_offset is not None:
            for r in range(sim.shape[0]): sim[r,exclude_self_offset[a+r]]=-1
        idx=np.argpartition(-sim,K,axis=1)[:,:K]; I[a:a+500]=idx; S[a:a+500]=np.take_along_axis(sim,idx,1)
    return I,S
def vote(I,S,lab):
    out=[]
    for i,s in zip(I,S):
        l=lab[i]; m=pd.notna(l)
        if not m.any(): out.append(np.nan); continue
        w=pd.Series(np.clip(s[m],0,None)+1e-6).groupby(l[m]).sum(); out.append(w.idxmax())
    return np.array(out,dtype=object)
F=pd.read_pickle(B+'fronts_final.pkl'); T=pd.read_pickle(B+'fronts_fine.pkl')
labF=pd.Series(C['r6.0'].values).where(pd.Series(C['r6.0'].values).isin(F.cluster)).values
labT=pd.Series(C['r20.0'].values).where(pd.Series(C['r20.0'].values).isin(T.cluster)).values
# validation on 2025 items: assign by neighbours excluding self
idx25=np.where(df.Year.values==2025)[0]; rng=np.random.default_rng(1); samp=rng.choice(idx25,4000,replace=False)
I,S=knn(Z[samp],exclude_self_offset=samp)
fv=vote(I,S,labF); ok=pd.notna(labF[samp])
print('front assignment accuracy (2025 holdout):', round(float((fv[ok]==labF[samp][ok]).mean()),3))
typ=F.set_index('cluster').type
print('type accuracy:', round(float((typ.reindex(fv[ok]).values==typ.reindex(labF[samp][ok]).values).mean()),3))
tv=vote(I,S,labT); ok2=pd.notna(labT[samp]); print('topic accuracy:', round(float((tv[ok2]==labT[samp][ok2]).mean()),3))
I,S=knn(Z26); d['front']=vote(I,S,labF); d['topic']=vote(I,S,labT); d['maxsim']=S.max(1)
print('2026 assigned fronts',d.front.notna().mean(),'median nn sim',np.median(d.maxsim))
d.to_pickle('d26a.pkl')

df=pd.read_pickle(B+'clean.pkl'); C=pd.read_pickle(B+'clusters_scan.pkl'); d=pd.read_pickle('d26a.pkl')
F=pd.read_pickle(B+'fronts_final.pkl'); T=pd.read_pickle(B+'fronts_fine.pkl')
df['front']=C['r6.0'].values; df['topic']=C['r20.0'].values
M=df.groupby(['jn','Year']).size().unstack(fill_value=0); bal=set(M.index[(M>0).all(1)]); print('balanced',len(bal))
n25=df[df.Year==2025].groupby('jn').size(); n26=d.groupby('jn').size()
cov=pd.DataFrame({'n25':n25,'n26':n26}).fillna(0).loc[sorted(bal)]
cov['ratio']=cov.n26/cov.n25
print('balanced journals with 0 items in 2026:', int((cov.n26==0).sum()), cov[cov.n26==0].index.tolist())
print('ratio 2026/2025 quartiles', cov.ratio.quantile([.1,.25,.5,.75,.9]).round(2).to_dict())
print('totals: all 2025',len(df[df.Year==2025]),'all 2026',len(d),'bal 2025',int(cov.n25.sum()),'bal 2026',int(cov.n26.sum()))
typ=F.set_index('cluster').type; jd=F.set_index('cluster').top_journal_share>50
order=['Emergent','Growing','Stable','Peaked','Declining']
a=df[(df.Year==2025)&df.jn.isin(bal)&df.front.isin(F.cluster)].copy(); a['type']=a.front.map(typ)
b=d[d.jn.isin(bal)&d.front.notna()].copy(); b['type']=b.front.map(typ)
w=(cov.n25/cov.n26).replace(np.inf,0); b['w']=b.jn.map(w)
def sh(x,wcol=None):
    s=x.groupby('type')[wcol].sum() if wcol else x.groupby('type').size(); return (s/s.sum()*100).reindex(order)
R={}
R['all_2025']=sh(a); R['all_2026']=sh(b); R['all_2026w']=sh(b,'w')
for t in ['C','A','P']:
    R[f'{t}_2025']=sh(a[a.tier==t]); R[f'{t}_2026']=sh(b[b.tier==t]); R[f'{t}_2026w']=sh(b[b.tier==t],'w')
R=pd.DataFrame(R).round(1); print(R.to_string())
EG=['Emergent','Growing']
for lab,x,wc in [('2025',a,None),('2026',b,None),('2026w',b,'w')]:
    xx=x[x.type.isin(EG)]; ww=xx[wc] if wc else pd.Series(1,index=xx.index)
    print(lab,'journal-driven share of E+G items', round(float(ww[xx.front.map(jd)].sum()/ww.sum()*100),1))
# tier shares full corpus
print('tier share 2025', (df[df.Year==2025].tier.value_counts(normalize=True)*100).round(1).to_dict(), '2026', (d.tier.value_counts(normalize=True)*100).round(1).to_dict())
# fronts: share change 2025->2026 (balanced, raw and weighted)
fa=a.groupby('front').size()/len(a)*100; fb=b.groupby('front').size()/len(b)*100; fbw=b.groupby('front').w.sum()/b.w.sum()*100
FF=F.set_index('cluster')[['terms','type','size','top_journal','top_journal_share','core']].join(pd.DataFrame({'s25':fa,'s26':fb,'s26w':fbw})).fillna(0)
FF['d']=FF.s26w-FF.s25
pd.set_option('display.width',250)
print(FF.sort_values('d',ascending=False).head(12).round(2).to_string()); print(FF.sort_values('d').head(10).round(2).to_string())
print(FF[FF.type=='Emergent'].round(2).to_string())
# type consistency: share of fronts whose 2026 change has the sign expected by type
FF['up']=FF.s26w>FF.s25
print(FF.groupby('type').up.mean().round(2).to_dict())
# LIS topics
Tt=T.set_index('cluster'); lis=Tt[(Tt.core+Tt.adj)>=50].index
ta=a[a.topic.isin(lis)] if 'topic' in a else None
a2=df[(df.Year==2025)&df.jn.isin(bal)&df.topic.isin(lis)].copy(); b2=d[d.jn.isin(bal)&d.topic.isin(lis)].copy(); b2['w']=b2.jn.map(w)
a2['type']=a2.topic.map(Tt.type); b2['type']=b2.topic.map(Tt.type)
print('LIS topics 2025',sh(a2).round(1).to_dict(),'2026w',sh(b2,'w').round(1).to_dict())
# novelty: max similarity to 2020-2025 items
Z=np.load(B+'Z.npy'); idx=np.where(df.Year.values==2025)[0]; rng=np.random.default_rng(2); s=rng.choice(idx,3000,replace=False)
base=np.concatenate([(lambda m:(m.__setitem__((np.arange(len(b)),b),-1),m.max(1))[1])(Z[b]@Z.T) for b in np.array_split(s,6)])
print('max-sim 2025 holdout median',round(float(np.median(base)),3),'p10',round(float(np.percentile(base,10)),3),' 2026 median',round(float(d.maxsim.median()),3),'p10',round(float(d.maxsim.quantile(.1)),3))
FF.to_pickle('fronts_2026.pkl'); R.to_pickle('types_2026.pkl'); cov.to_pickle('cov.pkl')

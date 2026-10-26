import numpy as np, pandas as pd, warnings, json; warnings.filterwarnings('ignore')
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import statsmodels.api as sm
import frontlib as L
df=L.df; Y=L.Y
M=df.groupby(['jn','Year']).size().unstack(fill_value=0); bal=M.index[(M>0).all(axis=1)]
df['bal']=df.jn.isin(bal)
C=pd.read_pickle('clusters_scan.pkl')
def features(part, base_mask, minsize=100):
    d=df[base_mask].copy(); d['cl']=part[base_mask.values]
    Nt=d.groupby('Year').size().reindex(Y).values.astype(float)
    rows=[]
    for c,g in d.groupby('cl'):
        if len(g)<minsize: continue
        n=g.groupby('Year').size().reindex(Y,fill_value=0).values.astype(float); t=np.arange(len(Y))
        lin=sm.GLM(n, sm.add_constant(t), family=sm.families.Poisson(), offset=np.log(Nt)).fit(scale='X2')
        br=sm.GLM(n, sm.add_constant(np.column_stack([t,(t==len(Y)-1).astype(float)])), family=sm.families.Poisson(), offset=np.log(Nt)).fit(scale='X2')
        st,stg=L.burst(n.astype(int), Nt.astype(int)); by=[Y[i] for i in range(len(Y)) if st[i]==1]
        tc=g.tier.value_counts(normalize=True); sh=n/Nt
        rows.append(dict(cluster=c,size=len(g),**{f'n{y}':int(v) for y,v in zip(Y,n)},**{f's{y}':v*100 for y,v in zip(Y,sh)},
          g_share=(np.exp(lin.params[1])-1)*100,g_lo=(np.exp(lin.params[1]-1.96*lin.bse[1])-1)*100,g_hi=(np.exp(lin.params[1]+1.96*lin.bse[1])-1)*100,g_p=lin.pvalues[1],
          break25=(np.exp(br.params[2])-1)*100,break25_p=br.pvalues[2],peak_year=Y[int(np.argmax(sh))],end_to_peak=sh[-1]/sh.max(),
          burst=('%d-%d'%(by[0],by[-1]) if by else ''),burst_strength=stg if by else 0,
          core=tc.get('C',0)*100,adj=tc.get('A',0)*100,periph=tc.get('P',0)*100,
          covid=g['COVID-19'].mean()*100,genai=g['GenAI'].mean()*100,ai=g['AI (broad)'].mean()*100,
          top_journal=g.jname.value_counts().index[0],top_journal_share=g.jname.value_counts(normalize=True).iloc[0]*100))
    F=pd.DataFrame(rows); P=np.log(F[[f's{y}' for y in Y]].values+1e-3); P=P-P.mean(1,keepdims=True)
    return F,P
if __name__=='__main__':
  F,P=features(C['r6.0'].values, df.bal)
  sil={k:silhouette_score(P,KMeans(k,n_init=50,random_state=0).fit(P).labels_) for k in range(3,9)}
  print('silhouette',{k:round(v,3) for k,v in sil.items()})
  km=KMeans(5,n_init=50,random_state=0).fit(P); F['tk']=km.labels_
  cent=np.exp(km.cluster_centers_)
  # name types by centroid shape
  names={}
  for j,cv in enumerate(cent):
      if cv[-1]>3: names[j]='Emergent surge'
      elif cv[-1]>1.25 and cv[-1]>cv[0]*1.5: names[j]='Sustained growth'
      elif np.argmax(cv)<=2 and cv[-1]<0.65: names[j]='Peaked'
      elif cv[-1]<cv[0]*0.8: names[j]='Declining'
      else: names[j]='Stable'
  print({names[j]:np.round(cv,2).tolist() for j,cv in enumerate(cent)}, names)
  F['type']=F.tk.map(names); F['terms']=F.cluster.map(L.ctfidf('micro', F.cluster.tolist())) if False else None
  L.df['micro']=C['r6.0'].values; F['terms']=F.cluster.map(L.ctfidf('micro',F.cluster.tolist()))
  F['centroid']=F.tk.map(lambda j: cent[j].round(3).tolist())
  F.to_pickle('fronts_bal.pkl')
  summ=F.groupby('type').agg(fronts=('cluster','size'),items=('size','sum'),g_med=('g_share','median'))
  summ['core_items_%']=F.groupby('type').apply(lambda x:(x['size']*x.core).sum()/x['size'].sum())
  summ['periph_items_%']=F.groupby('type').apply(lambda x:(x['size']*x.periph).sum()/x['size'].sum())
  print(summ.round(1))
  # robustness: other resolutions, map item-level types via same rule on their own k-means; compare item type agreement
  base_item=pd.Series(F.set_index('cluster').type).reindex(C['r6.0'].values).values
  agree={}
  for r in ['r3.0','r12.0']:
      F2,P2=features(C[r].values, df.bal)
      km2=KMeans(5,n_init=50,random_state=0).fit(P2); c2=np.exp(km2.cluster_centers_); n2={}
      for j,cv in enumerate(c2):
          if cv[-1]>3: n2[j]='Emergent surge'
          elif cv[-1]>1.25 and cv[-1]>cv[0]*1.5: n2[j]='Sustained growth'
          elif np.argmax(cv)<=2 and cv[-1]<0.65: n2[j]='Peaked'
          elif cv[-1]<cv[0]*0.8: n2[j]='Declining'
          else: n2[j]='Stable'
      F2['type']=km2.labels_; F2['type']=F2.type.map(n2)
      it=pd.Series(F2.set_index('cluster').type).reindex(C[r].values).values
      m=df.bal.values & pd.notna(base_item) & pd.notna(it)
      agree[r]=dict(fronts=len(F2), agreement=float((base_item[m]==it[m]).mean()), types=sorted(set(n2.values())))
  print('robustness',agree)
  json.dump(dict(sil=sil,agree=agree),open('fronts_meta.json','w'),default=str)

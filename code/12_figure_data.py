"""Collect the numbers plotted in the manuscript figures into figdata.json."""
import json, pandas as pd, numpy as np
Y=list(range(2016,2026)); df=pd.read_pickle('clean.pkl')
tc=df.groupby(['Year','tier']).size().unstack()
drop=['library philosophy and practice','webology']
core_excl=df[(df.tier=='C')&~df.jn.isin(drop)].groupby('Year').size().reindex(Y).tolist()
CL=pd.read_pickle('clusters_scan.pkl'); df['front']=CL['r6.0'].values
F=pd.read_pickle('fronts_final.pkl'); tmap=F.set_index('cluster').type
M=df.groupby(['jn','Year']).size().unstack(fill_value=0); bal=M.index[(M>0).all(axis=1)]
d=df[df.jn.isin(bal)].copy(); d['ft']=d.front.map(tmap); d=d[d.ft.notna()]
comp={}
for t in 'CAP':
    x=d[d.tier==t].groupby(['Year','ft']).size().unstack().fillna(0); x=x.div(x.sum(axis=1),axis=0)*100
    comp[t]={k:x[k].round(2).tolist() for k in x.columns}
# topics shown in Figs 5 and 6, identified by their distinctive terms (robust to cluster numbering)
T=pd.read_pickle('fronts_fine.pkl'); T=T[(T.core+T.adj)>=50]
SEL=[('Emergent','Large language models','large language'),('Emergent','Generative AI','generative ai'),('Emergent','AI in libraries','ai libraries'),
 ('Emergent','AI ethics','ethical'),('Emergent','Knowledge graphs and graph neural networks','knowledge graph'),('Emergent','Digital transformation','digital transformation'),
 ('Emergent','Sustainable development','sustainable development'),('Emergent','Virtual cultural heritage','cultural heritage'),('Emergent','Workplace and employees','job satisfaction'),
 ('Growing','Research integrity and retractions','retraction'),('Growing','Systematic reviews','systematic literature'),('Growing','Gender in science','gender gap'),
 ('Growing','Online health communities','online health'),('Growing','Indigenous knowledge','indigenous'),('Growing','Digital platforms','digital platforms'),
 ('Growing','Technology acceptance','utaut'),('Growing','Diversity, equity, and inclusion','equity inclusion'),('Growing','Bibliometric mapping','vosviewer'),('Growing','Interdisciplinarity','interdisciplinary'),
 ('Peaked','Pandemic library services','libraries covid'),('Peaked','COVID-19 and misinformation','misinformation'),('Peaked','Health sciences libraries','health sciences'),
 ('Peaked','University rankings','university rankings'),('Peaked','Open educational resources','open educational'),('Peaked','Library programs for children','storytime'),
 ('Declining','Electronic resources','e-resources'),('Declining','Cataloging and metadata','cataloging'),('Declining','Information retrieval','information retrieval'),
 ('Declining','Reference services','reference services'),('Declining','Information literacy instruction','literacy instruction'),('Declining','Collection development','collection development'),
 ('Declining','Digital humanities','digital humanities'),('Declining','Journal impact factors','journal impact'),('Declining','Open access','access publishing'),
 ('Declining','Information seeking','information seeking'),('Declining','Citation analysis','h-index'),('Declining','Institutional repositories','institutional repositories'),('Declining','Altmetrics','altmetric')]
topics=[]
for typ,lab,term in SEL:
    c=T[(T.type==typ)&T.terms.str.contains(term,regex=False)].sort_values('size',ascending=False)
    if len(c)==0: print('not found:',lab); continue
    r=c.iloc[0]; topics.append(dict(cluster=int(r.cluster),type=typ,label=lab,s=[round(r[f's{y}'],4) for y in Y],g=round(r.g_share,1),core=round(r.core,1)))
json.dump({'tier_counts':{k:tc[k].tolist() for k in tc},'core_excl':core_excl,'comp':comp,'topics':topics},open('figdata.json','w'))
print('figdata.json written;', len(topics), 'topics')

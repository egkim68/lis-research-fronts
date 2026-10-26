import numpy as np, pandas as pd, json
F=pd.read_pickle('fronts_final.pkl'); import frontlib as L; Y=L.Y
df=pd.read_pickle('clean.pkl'); CL=pd.read_pickle('clusters_scan.pkl'); df['front']=CL['r6.0'].values
M=df.groupby(['jn','Year']).size().unstack(fill_value=0); bal=M.index[(M>0).all(axis=1)]; d=df[df.jn.isin(bal)]
def classify(r,E=3,rise=1.15,dec=0.6,alpha=0.05): return L.typ(r,E=E,rise=rise,fall=dec,alpha=alpha)
sc=[('Main specification',{}),('Emergence threshold 2x',{'E':2}),('Emergence threshold 4x',{'E':4}),
    ('Peak rise 10%',{'rise':1.10}),('Peak rise 25%',{'rise':1.25}),('Peak decline to 50% of peak',{'dec':0.5}),('Peak decline to 70% of peak',{'dec':0.7}),('Significance p < 0.10',{'alpha':0.10}),('Significance p < 0.01',{'alpha':0.01})]
rows=[]
for name,kw in sc:
    t=F.apply(lambda r: classify(r,**kw),axis=1); tm=dict(zip(F.cluster,t))
    eg=t.isin(['Emergent','Growing']); jd=F.top_journal_share>50
    s20=F.loc[eg,f's{Y[0]}'].sum(); s25=F.loc[eg,'s2025'].sum()
    gain=(F.loc[eg,'s2025']-F.loc[eg,f's{Y[0]}']).sum(); gjd=(F.loc[eg&jd,'s2025']-F.loc[eg&jd,f's{Y[0]}']).sum()
    dec=t=='Declining'; core_dec=(F.loc[dec,'size']*F.loc[dec,'core']).sum()/F.loc[dec,'size'].sum()
    eg_per=(F.loc[eg,'size']*F.loc[eg,'periph']).sum()/F.loc[eg,'size'].sum()
    dd=d.assign(ft=d.front.map(tm)); dc=dd[(dd.tier=='C')&dd.ft.notna()]
    sh=dc.groupby(['Year','ft']).size().unstack().fillna(0); sh=sh.div(sh.sum(axis=1),axis=0)*100
    rows.append(dict(scenario=name, emergent=(t=='Emergent').sum(), growing=(t=='Growing').sum(), stable=(t=='Stable').sum(), peaked=(t=='Peaked').sum(), declining=dec.sum(),
       eg_first=round(s20,1), eg_2025=round(s25,1), jd_share_of_gain=round(100*gjd/gain,1), eg_periph=round(eg_per,1), declining_core=round(core_dec,1),
       core_in_declining_first=round(sh.loc[Y[0]].get('Declining',0),1), core_in_declining_2025=round(sh.loc[2025].get('Declining',0),1)))
R=pd.DataFrame(rows); pd.set_option('display.width',250); print(R.to_string()); R.to_csv('threshold_sensitivity.csv',index=False)
print('emergent fronts with significant positive g:', F[F.type=='Emergent'][['terms','g_share','g_p']].round(4).to_string())

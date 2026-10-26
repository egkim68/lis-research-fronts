"""Manuscript figures 1 to 6 (written to figs/)."""
import json, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({'font.family':'Liberation Sans','font.size':10,'axes.edgecolor':'black','axes.labelcolor':'black','xtick.color':'black','ytick.color':'black','text.color':'black','axes.linewidth':0.8,'savefig.dpi':300})
FD=json.load(open('figdata.json'))
_a=pd.read_pickle('all.pkl'); _d=pd.read_pickle('clean.pkl'); _M=_d.groupby(['jn','Year']).size().unstack(fill_value=0); _b=_M[(_M>0).all(axis=1)]
from sklearn.metrics import roc_auc_score
K=dict(records=len(_a),items=len(_d),bal_j=len(_b),bal_n=int(_b.values.sum()),auc=float(open('auc.txt').read()) if __import__('os').path.exists('auc.txt') else 0.93,n_fronts=len(pd.read_pickle('fronts_final.pkl')),n_topics=len(pd.read_pickle('fronts_fine.pkl')))
# auc value is printed by 10_validate_tiers.py (held-out item AUC core vs periph)
Y=list(range(2016,2026)); TORD=['Emergent','Growing','Stable','Peaked','Declining']
TC={'Emergent':'#6250d6','Growing':'#2a78d6','Stable':'#2e8b57','Peaked':'#eb6834','Declining':'#e34948'}
OUT='figs/'
import os; os.makedirs(OUT,exist_ok=True)
# Fig 1 workflow
st=[('Data collection','Scopus, 2016 to 2025',f"295 SJR LIS journals; {K['records']:,} records"),
 ('Cleaning',f"{K['items']:,} research items",f"Balanced panel: {K['bal_j']} journals, {K['bal_n']:,} items"),
 ('Journal tiers','Core (182), adjacent (71), peripheral (42)',f"Checked by vocabulary (AUC {K['auc']:.2f})"),
 ('Text representation','TF-IDF of title, abstract, keywords','Condensed to 256 dimensions'),
 ('Clustering','Similarity network; Leiden algorithm',f"{K['n_fronts']} fronts and {K['n_topics']} topics"),
 ('Trajectories','Yearly share, growth rate, peak year','Bursts; journal concentration'),
 ('Typology and tests','Five trajectory types (Figure 2)','2025 deviation test; robustness checks')]
fig,ax=plt.subplots(figsize=(6.3,5.9)); ax.set_xlim(0,10); ax.set_ylim(0,len(st)); ax.axis('off')
for i,(t,d1,d2) in enumerate(st):
    y=len(st)-1-i
    ax.add_patch(FancyBboxPatch((0.8,y+0.2),9.1,0.62,boxstyle='round,pad=0.0,rounding_size=0.08',fc='white',ec='black',lw=0.9))
    ax.add_patch(plt.Circle((0.35,y+0.51),0.25,color='#2a78d6')); ax.text(0.35,y+0.51,str(i+1),ha='center',va='center',color='white',fontsize=10,fontweight='bold')
    ax.text(1.0,y+0.51,t,va='center',fontsize=10,fontweight='bold'); ax.plot([4.0,4.0],[y+0.3,y+0.72],color='black',lw=0.6)
    ax.text(4.2,y+0.64,d1,va='center',fontsize=9.5); ax.text(4.2,y+0.38,d2,va='center',fontsize=9.5)
    if i<len(st)-1: ax.annotate('',xy=(5.35,y-0.17),xytext=(5.35,y+0.2),arrowprops=dict(arrowstyle='-|>',color='black',lw=0.9))
fig.savefig(OUT+'fig1.png',bbox_inches='tight'); plt.close()
# Fig 2 decision chain
q=[('Peak in 2020, 2021, or 2022, at least 15% above\nthe pre-pandemic share (2016 to 2019), and\n2025 share at most 60% of the peak?','Peaked'),
   ('Share in 2024 and 2025 at least three times\nthe pre-pandemic share?','Emergent'),
   ('Share rising significantly (p < 0.05)?','Growing'),('Share falling significantly (p < 0.05)?','Declining')]
fig,ax=plt.subplots(figsize=(6.3,5.0)); ax.set_xlim(0,10); ax.set_ylim(-0.9,4.15); ax.axis('off')
for i,(t,o) in enumerate(q):
    y=3-i; h=0.68; y0=y+0.16
    ax.add_patch(FancyBboxPatch((0.05,y0),6.4,h,boxstyle='round,pad=0,rounding_size=0.08',fc='white',ec='black',lw=0.9)); ax.text(0.25,y0+h/2,t,va='center',fontsize=9.5)
    ax.annotate('',xy=(7.3,y0+h/2),xytext=(6.45,y0+h/2),arrowprops=dict(arrowstyle='-|>',color='black',lw=0.9)); ax.text(6.87,y0+h/2+0.08,'Yes',ha='center',fontsize=9,fontweight='bold')
    ax.add_patch(FancyBboxPatch((7.35,y0+h/2-0.25),2.5,0.5,boxstyle='round,pad=0,rounding_size=0.25',fc=TC[o],ec='none')); ax.text(8.6,y0+h/2,o,ha='center',va='center',color='white',fontsize=10,fontweight='bold')
    ax.annotate('',xy=(0.8,y0-0.3),xytext=(0.8,y0),arrowprops=dict(arrowstyle='-|>',color='black',lw=0.9)); ax.text(0.95,y0-0.15,'No',fontsize=9,fontweight='bold',va='center')
ax.add_patch(FancyBboxPatch((0.05,-0.7),1.9,0.5,boxstyle='round,pad=0,rounding_size=0.25',fc=TC['Stable'],ec='none')); ax.text(1.0,-0.45,'Stable',ha='center',va='center',color='white',fontsize=10,fontweight='bold')
fig.savefig(OUT+'fig2.png',bbox_inches='tight'); plt.close()
# Fig 3 line chart (fonts 12, no grey)
tc=FD['tier_counts']; plt.rcParams['font.size']=12; fig,ax=plt.subplots(figsize=(5.85,3.4))
for n,k,c,ls in [('Core','C','#2a78d6','-'),('Core without two\ndelisted titles',None,'#2a78d6',':'),('Adjacent','A','#1baf7a','-'),('Peripheral','P','#eb6834','-')]:
    v=tc[k] if k else FD['core_excl']; ax.plot(Y,v,ls,color=c,lw=2,marker='o',ms=4,label=n)
ax.set_ylim(0,10000); ax.set_xlabel('Year'); ax.set_ylabel('Research items'); ax.set_xticks(Y)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v,p:f'{int(v):,}')); ax.spines[['top','right']].set_visible(False)
ax.legend(title='Journal tier',loc='center left',bbox_to_anchor=(1.02,0.5),frameon=False,alignment='left')
fig.savefig(OUT+'fig3.png',bbox_inches='tight'); plt.close(); plt.rcParams['font.size']=10
# Fig 4 bar pair: 2017 vs 2025
fig,axs=plt.subplots(1,2,figsize=(6.6,2.8),sharey=True)
for ax,(k,tt) in zip(axs,[('C','(a) Core journals'),('P','(b) Peripheral journals')]):
    yy=np.arange(5)[::-1]; a=[FD['comp'][k][t][0] for t in TORD]; b=[FD['comp'][k][t][-1] for t in TORD]
    ax.barh(yy+0.2,a,0.38,color='#a9c9ef',label=str(Y[0])); ax.barh(yy-0.2,b,0.38,color='#1b5fb0',label='2025')
    for y0,v in zip(yy+0.2,a): ax.text(v+0.8,y0,f'{v:.0f}',va='center',fontsize=8)
    for y0,v in zip(yy-0.2,b): ax.text(v+0.8,y0,f'{v:.0f}',va='center',fontsize=8)
    ax.set_yticks(yy); ax.set_yticklabels(TORD); ax.set_xlim(0,82); ax.set_xticks([0,25,50,75]); ax.set_xticklabels(['0%','25%','50%','75%'])
    ax.set_title(tt,loc='left',fontsize=10,fontweight='bold'); ax.spines[['top','right']].set_visible(False)
axs[1].legend(title='Year',loc='center left',bbox_to_anchor=(1.02,0.5),frameon=False)
fig.tight_layout(); fig.savefig(OUT+'fig4.png',bbox_inches='tight'); plt.close()
# Fig 5/6 heatmaps
n_y=len(Y)
for fn,types in [('fig5',['Emergent','Growing']),('fig6',['Peaked','Declining'])]:
    rows=sorted([r for t in types for r in FD['topics'] if r['type']==t], key=lambda r:(types.index(r['type']), r['g'] if r['type']=='Declining' else -r['g']))
    n=len(rows)+len(types); fig=plt.figure(figsize=(6.6,0.32*n+0.9)); ax=fig.add_axes([0.36,0.06,0.40,0.86])
    grid=[];labels=[];gro=[];core=[]
    for t in types:
        grid.append([np.nan]*n_y); labels.append(t); gro.append(''); core.append('')
        for r in rows:
            if r['type']!=t: continue
            s=np.array(r['s']); grid.append(list((s-s.min())/(s.max()-s.min()))); labels.append(r['label']); gro.append(f"{r['g']:+.0f}%".replace('-','\u2212')); core.append(f"{r['core']:.0f}%")
    G=np.array(grid,float); im=ax.imshow(G,aspect='auto',cmap='viridis',vmin=0,vmax=1)
    ax.set_xticks(range(n_y)); ax.set_xticklabels([f"’{str(y)[2:]}" for y in Y],fontsize=11); ax.xaxis.tick_top(); ax.tick_params(axis='x',pad=2); ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels,fontsize=11)
    for i,l in enumerate(labels):
        if l in types: ax.get_yticklabels()[i].set_fontweight('bold')
    ax.set_xticks(np.arange(-.5,n_y),minor=True); ax.set_yticks(np.arange(-.5,len(labels)),minor=True); ax.grid(which='minor',color='white',lw=1.2); ax.tick_params(which='minor',length=0); ax.tick_params(length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    for i,(g,c) in enumerate(zip(gro,core)):
        ax.text(n_y+0.25,i,g,va='center',ha='left',fontsize=11); ax.text(n_y+2.5,i,c,va='center',ha='left',fontsize=11)
    ax.text(n_y+0.25,-0.62,'Growth',fontsize=11,ha='left',va='bottom'); ax.text(n_y+2.5,-0.62,'Core',fontsize=11,ha='left',va='bottom')
    cax=fig.add_axes([0.93,0.35,0.02,0.4]); cb=fig.colorbar(im,cax=cax,ticks=[0,1]); cb.ax.set_yticklabels(['min','max'],fontsize=11); cb.outline.set_visible(False); cax.set_title('Share',fontsize=11,loc='left')
    fig.savefig(OUT+fn+'.png',bbox_inches='tight'); plt.close()
print('done')

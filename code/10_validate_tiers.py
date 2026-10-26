import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score, confusion_matrix
df=pd.read_pickle('clean.pkl'); Z=np.load('Z.npy')
y=df.tier.values; g=df.jn.values
# (1) core vs peripheral, journal-held-out (grouped 5-fold): AUC on items of unseen journals
m=np.isin(y,['C','P']); Xc,yc,gc=Z[m],(y[m]=='C').astype(int),g[m]
pred=np.zeros(len(yc))
for tr,te in GroupKFold(5).split(Xc,yc,gc):
    clf=LogisticRegression(max_iter=2000,C=1.0,class_weight='balanced').fit(Xc[tr],yc[tr]); pred[te]=clf.predict_proba(Xc[te])[:,1]
auc=round(roc_auc_score(yc,pred),3); print('held-out item AUC core vs periph', auc); open('auc.txt','w').write(str(auc))
jj=pd.DataFrame({'jn':gc,'y':yc,'p':pred}).groupby('jn').agg(y=('y','first'),p=('p','mean'),n=('y','size'))
jj['pred']=(jj.p>0.5).astype(int); print('journal-level agreement C vs P', round((jj.pred==jj.y).mean(),3), len(jj))
print('misclassified', jj[jj.pred!=jj.y].sort_values('n',ascending=False).head(10))
# (2) three-tier, journal held-out multinomial; journal = mean probs
lab={'C':0,'A':1,'P':2}; Y3=np.array([lab[t] for t in y]); P3=np.zeros((len(y),3))
for tr,te in GroupKFold(5).split(Z,Y3,g):
    clf=LogisticRegression(max_iter=3000,C=1.0,class_weight='balanced').fit(Z[tr],Y3[tr]); P3[te]=clf.predict_proba(Z[te])
J=pd.DataFrame(P3,columns=['C','A','P']); J['jn']=g; J['y']=y; Jm=J.groupby('jn').agg(C=('C','mean'),A=('A','mean'),P=('P','mean'),y=('y','first'),n=('y','size'))
Jm['pred']=Jm[['C','A','P']].idxmax(axis=1)
cm=pd.crosstab(Jm.y,Jm.pred); print(cm); print('three-tier journal agreement', round((Jm.pred==Jm.y).mean(),3))
Jm.to_csv('journal_validation.csv')

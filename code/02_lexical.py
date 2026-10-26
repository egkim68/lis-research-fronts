import pandas as pd, numpy as np, scipy.sparse as sp, pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
EXTRA = set('''purpose design methodology approach findings originality value implications limitations significance method process result conclusion results conclusions paper study studies research article articles based using used use also aims aim objective objectives proposed present presents provide provides provided show shows shown new data analysis la el en del da de las los le les des et une un para por con que se al di il della dei che per una um uma em os dos das na no nas nos ao para pelo pela sobre como mais entre esta este und der die das zu von mit den im ist sich auf für ein eine'''.split())
STOP = list(ENGLISH_STOP_WORDS | EXTRA)
df = pd.read_pickle('clean.pkl')
vec = TfidfVectorizer(stop_words=STOP, min_df=10, max_df=0.4, ngram_range=(1,2), max_features=60000, sublinear_tf=True, token_pattern=r'(?u)\b[a-z][a-z\-]+\b')
X = vec.fit_transform(df.text)
sp.save_npz('X.npz', X); pickle.dump(vec, open('vec.pkl','wb'))
core = (df.tier=='C').values
# journal centroids
J = df.jn.values; js = pd.unique(J)
cent = {}
for j in js:
    idx = np.where(J==j)[0]; cent[j] = np.asarray(X[idx].sum(0)).ravel(); 
coresum = sum(cent[j] for j in js if (df.tier[df.jn==j].iloc[0]=='C'))
persum = sum(cent[j] for j in js if (df.tier[df.jn==j].iloc[0]=='P'))
rows=[]
for j in js:
    t = df.tier[df.jn==j].iloc[0]
    c = coresum - cent[j] if t=='C' else coresum   # leave-one-out
    p = persum - cent[j] if t=='P' else persum
    v = cent[j]/np.linalg.norm(cent[j])
    sc = v@c/np.linalg.norm(c); spr = v@p/np.linalg.norm(p)
    rows.append((j, df.jname[df.jn==j].iloc[0], t, df.domain[df.jn==j].iloc[0], (J==j).sum(), sc, spr))
r = pd.DataFrame(rows, columns=['jn','journal','tier','domain','n','sim_core','sim_periph'])
r['lis_index'] = r.sim_core - r.sim_periph
r.to_csv('journal_lexical.csv', index=False)
print(r.groupby('tier')[['sim_core','sim_periph','lis_index']].describe().T.round(3))
pd.set_option('display.width',220); pd.set_option('display.max_rows',100)
print('Core journals with lowest index'); print(r[r.tier=='C'].nsmallest(15,'lis_index')[['journal','n','sim_core','lis_index']])
print('Adjacent highest'); print(r[r.tier=='A'].nlargest(10,'lis_index')[['journal','n','sim_core','lis_index']])
print('Peripheral highest'); print(r[r.tier=='P'].nlargest(10,'lis_index')[['journal','n','sim_core','lis_index']])
# article-level LIS index: cosine to leave-in core centroid minus periph centroid
cc = normalize(coresum.reshape(1,-1)).ravel(); pc = normalize(persum.reshape(1,-1)).ravel()
df['lis_idx'] = X@cc - X@pc
df[['EID','lis_idx']].to_pickle('artlis.pkl')
from sklearn.metrics import roc_auc_score
m = df.tier.isin(['C','P'])
print('AUC article-level core vs periph:', roc_auc_score(df.tier[m]=='C', df.lis_idx[m]))

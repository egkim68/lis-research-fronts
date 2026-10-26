import numpy as np, scipy.sparse as sp, pandas as pd, igraph as ig, leidenalg as la, sys
I=np.load('knnI.npy'); S=np.load('knnS.npy'); n,K=I.shape
rows=np.repeat(np.arange(n),K); A=sp.coo_matrix((np.clip(S.ravel(),0,None),(rows,I.ravel())),shape=(n,n)).tocsr(); A=A.maximum(A.T).tocoo(); m=A.row<A.col
g=ig.Graph(n=n, edges=np.column_stack([A.row[m],A.col[m]]).tolist(), edge_attrs={'weight':A.data[m].tolist()})
res={}
for r in [float(x) for x in sys.argv[1:]]:
    p = la.find_partition(g, la.RBConfigurationVertexPartition, weights='weight', resolution_parameter=r, seed=42, n_iterations=5)
    lab=np.array(p.membership); sz=np.bincount(lab)
    print(r, 'clusters', len(sz), 'n>=100', (sz>=100).sum(), 'cover>=100', round(sz[sz>=100].sum()/n,3), 'median(>=100)', int(np.median(sz[sz>=100])), 'max', sz.max(), flush=True)
    res[f'r{r}']=lab
pd.DataFrame(res).to_pickle('clusters_scan.pkl')

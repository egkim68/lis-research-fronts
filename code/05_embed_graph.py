"""256-dimensional SVD of the TF-IDF matrix and 15-nearest-neighbour graph (cosine)."""
import numpy as np, scipy.sparse as sp, time, pandas as pd, igraph as ig, leidenalg as la
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
X = sp.load_npz('X.npz'); t=time.time()
Z = TruncatedSVD(n_components=256, random_state=7).fit_transform(X); Z = normalize(Z).astype(np.float32)
np.save('Z.npy', Z); print('svd', time.time()-t)
K=15; n=Z.shape[0]; I=np.zeros((n,K),np.int32); S=np.zeros((n,K),np.float32)
for a in range(0,n,500):
    sim = Z[a:a+500]@Z.T
    for r in range(sim.shape[0]): sim[r,a+r] = -1
    idx = np.argpartition(-sim, K, axis=1)[:,:K]
    I[a:a+500]=idx; S[a:a+500]=np.take_along_axis(sim, idx, 1)
print('knn', time.time()-t)
np.save('knnI.npy',I); np.save('knnS.npy',S)
print('saved knnI.npy, knnS.npy, Z.npy')

import numpy as np
X = np.array([
 [5,3,0,1],
 [4,0,0,1],
 [1,1,0,5],
 [1,0,0,4],
 [0,1,5,4],])
from sklearn.decomposition import NMF
model = NMF(n_components=2, init='random', random_state=0)
model.fit(X)
'''NMF(alpha=0.0, beta=1, eta=0.1, init='random', l1_ratio=0.0, max_iter=200,
    n_components=2, nls_max_iter=2000, random_state=0, shuffle=False,
    solver='cd', sparseness=None, tol=0.0001, verbose=0)'''



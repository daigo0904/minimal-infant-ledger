import sys, numpy as np
sys.path.insert(0, '../S190_なぐさめの代価_20261121')
from multiprocessing import Pool
from 共 import *
def one(job):
    s, x = job; o = 一生(s, 'v4', なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=x); A, 相 = o['行動列'][7000:], o['相手列'][7000:]
    return 泣きなぐさめ(o, 7000, 8000) + (float((A[相 > 0] == 3).mean()), float(o['食列'][7000:].mean()))
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        R = {x: np.array(p.map(one, [(s, x) for s in range(900, 910)], chunksize=1)) for x in [0.0, 0.01, 0.03]}
    for x, r in R.items():
        m = np.nanmedian(r, 0); print(f'代価{x}: 泣いている−いない {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） 泣いている時 {m[1]:.3f} いない時 {m[2]:.3f} 仲間の前の手3 {m[6]:.3f} 相手>0.5 {m[3]:.3f} 食べ {m[7]:.4f}')
    for x in [0.01, 0.03]: print(f'代価{x} 手3 < 代価0: {int((R[x][:,6] < R[0.0][:,6]).sum())}/10  差 > 代価0: {int((R[x][:,0] > R[0.0][:,0]).sum())}/10')

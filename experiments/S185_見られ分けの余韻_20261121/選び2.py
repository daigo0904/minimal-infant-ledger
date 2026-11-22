import sys, numpy as np
sys.path.insert(0, '../S185_見られ分けの余韻_20261121')
from multiprocessing import Pool
from 共 import *
def one(job): s, 名, α = job; o = 一生(s, 名, 記憶=α); return 余韻(o, 7000, 8000) + (float(o['食列'][7000:].mean()),)
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        R = {α: np.array(p.map(one, [(s, '元', α) for s in range(900, 910)], chunksize=1)) for α in [None, 0.5]}
    for α, r in R.items():
        m = np.median(r, 0); print(f'元 記憶{α}: 余韻 {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） 直後 {m[1]:.3f} 続き {m[2]:.3f} 見られ分け {m[3]:+.3f} 食べ {m[4]:.4f}')
    print('余韻 記憶0.5 > なし:', int((R[0.5][:, 0] > R[None][:, 0]).sum()), '/10')

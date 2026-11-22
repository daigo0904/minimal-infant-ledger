import sys, numpy as np
sys.path.insert(0, '../S168_見て学ぶ_20261120')
from multiprocessing import Pool
from 共 import *
def one(job):
    s, 名, k = job; o = 一生(s, '見る', 名, 種類=(4000,), k代理=k)
    return tuple(種類の差(o, s, 4000, lo, hi) for lo, hi in [(3000, 4000), (4000, 4300), (4000, 4600), (7000, 8000)]) + (float(o['食列'][4000:5000].mean()),)
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        R = {}
        for 名, k in [('元', 0.0), ('v4', 0.0), ('v4', 1.0), ('v4', 3.0)]:
            r = np.array(p.map(one, [(s, 名, k) for s in range(900, 910)], chunksize=1)); R[(名, k)] = r; m = np.median(r, 0)
            print(f'{名} 代理{k}: 種類の差 前半の終わり {m[0]:+.3f} 後半 4000-4300 {m[1]:+.3f} 4000-4600 {m[2]:+.3f} 7000-8000 {m[3]:+.3f} 食べ(4000-5000) {m[4]:.4f}', flush=True)
        for k in [1.0, 3.0]:
            print(f'代理{k} > 代理0（4000-4300）:', int((R[('v4', k)][:, 1] > R[('v4', 0.0)][:, 1]).sum()), '/10  （4000-4600）:', int((R[('v4', k)][:, 2] > R[('v4', 0.0)][:, 2]).sum()), '/10')

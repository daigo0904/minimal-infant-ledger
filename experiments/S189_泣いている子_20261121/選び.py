import sys, numpy as np
sys.path.insert(0, '../S189_泣いている子_20261121')
from multiprocessing import Pool
from 共 import *
def one(job): s, k, x = job; o = 一生(s, 'v4', なぐさめ=True, kE=k, 共感型='苦しさ', 泣き=x); return 泣きなぐさめ(o, 7000, 8000) + (float(o['食列'][7000:].mean()),)
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for x in [0.0, 0.005, 0.01]:
            for k in [0.0, 50.0]:
                r = np.array(p.map(one, [(s, k, x) for s in range(900, 910)], chunksize=1)); m = np.nanmedian(r, 0)
                print(f'泣き{x} kE{k}: なぐさめ 泣いている−いない {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） 泣いている時 {m[1]:.3f} いない時 {m[2]:.3f} ／ 相手 >0.5 の割合 {m[3]:.3f} 90%点 {m[4]:.2f} 中央値 {m[5]:.2f} 食べ {m[6]:.4f}', flush=True)

import sys, numpy as np
sys.path.insert(0, '../S185_見られ分けの余韻_20261121')
from multiprocessing import Pool
from 共 import *
def one(job): s, 名, α = job; o = 一生(s, 名, 記憶=α); return 余韻(o, 7000, 8000) + (float(o['食列'][7000:].mean()),)
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for 名, α in [('v4', None), ('v4', 0.5), ('v4', 0.2), ('元', 0.5)]:
            r = np.array(p.map(one, [(s, 名, α) for s in range(900, 910)], chunksize=1)); m = np.median(r, 0)
            print(f'{名} 記憶{α}: 余韻（直後−続き）{m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） 直後 {m[1]:.3f} 続き {m[2]:.3f} 見られ分け {m[3]:+.3f} 食べ {m[4]:.4f}', flush=True)

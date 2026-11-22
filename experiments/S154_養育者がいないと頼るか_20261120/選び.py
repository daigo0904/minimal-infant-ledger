import sys, numpy as np
sys.path.insert(0, '../S154_養育者がいないと頼るか_20261120')
from multiprocessing import Pool
from 共 import *
def one(job): s, 参照, 正直 = job; o = 一生(s, 参照, 'v4', 物知り=(1, 正直)); return 数える(o, 6000, 8000) + (o['sha256'],)
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        rs = {}
        for 参照 in ['養育者', 'ずらし']:
            for 正直 in [1.0, 0.7, 0.5]:
                r = p.map(one, [(s, 参照, 正直) for s in range(900, 910)], chunksize=1); rs[(参照, 正直)] = r
                m = np.median(np.array([x[:4] for x in r]), 0)
                print(f'{参照} 正直さ{正直}: 養育者 {m[0]:+.3f} 物知り {m[1]:+.3f} ほか {m[2]:+.3f} 食べ {m[3]:.4f}', flush=True)
        print('sha 養育者≠ずらし(0.7):', sum(a[4] != b[4] for a, b in zip(rs[('養育者', 0.7)], rs[('ずらし', 0.7)])), '/10')
        print('0.7物知り ずらし>養育者:', sum(b[1] > a[1] for a, b in zip(rs[('養育者', 0.7)], rs[('ずらし', 0.7)])), '/10')
        print('1.0物知り ずらし>養育者:', sum(b[1] > a[1] for a, b in zip(rs[('養育者', 1.0)], rs[('ずらし', 1.0)])), '/10')
        print('ずらし 0.7>0.5:', sum(a[1] > b[1] for a, b in zip(rs[('ずらし', 0.7)], rs[('ずらし', 0.5)])), '/10')

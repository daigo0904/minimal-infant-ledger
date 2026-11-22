import sys, numpy as np
sys.path.insert(0, '../S170_失敗を見せる仲間_20261120')
from multiprocessing import Pool
from 数え import 測る
def one(job): return 測る(*job)[:5]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {(k, n): np.array(p.map(one, [(s, k, n) for s in range(900, 910)], chunksize=1)) for k in [0.0, 3.0] for n in [None, 1]}
    for (k, n), r in R.items():
        m = np.median(r, 0); print(f'代理{k} 何でも{n}: 良いを取る {m[0]:.3f} 悪いを取る {m[1]:.3f} 初めて悪いまで {m[2]:.1f} 悪い取り {m[3]:.1f} 食べ {m[4]:.4f}')
    a, b, c = R[(3.0, 1)], R[(3.0, None)], R[(0.0, 1)]
    print('悪いを取る 代理3＋何でも < 代理3のみ:', int((a[:, 1] < b[:, 1]).sum()), '/10  < 代理0＋何でも:', int((a[:, 1] < c[:, 1]).sum()), '/10')
    print('（代理3−代理0）の悪いを取る差 何でもあり < なし:', int(((a[:, 1] - c[:, 1]) < (b[:, 1] - R[(0.0, None)][:, 1])).sum()), '/10  初めて悪いまで 代理3＋何でも > 代理0＋何でも:', int((a[:, 2] > c[:, 2]).sum()), '/10')

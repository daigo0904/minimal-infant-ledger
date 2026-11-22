import sys, numpy as np
sys.path.insert(0, '../S169_見て避ける_20261120')
from multiprocessing import Pool
from 数え import 測る
def one(job): return 測る(*job)[:7]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in [0.0, 3.0]}
    for k, r in R.items():
        m = np.median(r, 0); print(f'代理{k}: 4000-4600 良いを取る {m[0]:.3f} 悪いを取る {m[1]:.3f} ／ 前半の終わり 良い {m[2]:.3f} 悪い {m[3]:.3f} ／ 初めて悪いを取るまで {m[4]:.0f}手 4000-4600 の悪い取り {m[5]:.1f}回 食べ {m[6]:.4f}')
    a, b = R[3.0], R[0.0]
    print('良いを取る 代理3>0:', int((a[:, 0] > b[:, 0]).sum()), '/10  悪いを取る 代理3<0:', int((a[:, 1] < b[:, 1]).sum()), '/10  初めて悪いまで 代理3>0:', int((a[:, 4] > b[:, 4]).sum()), '/10  悪い取りの回数 代理3<0:', int((a[:, 5] < b[:, 5]).sum()), '/10')

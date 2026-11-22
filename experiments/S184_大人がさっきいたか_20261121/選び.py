import sys, numpy as np
sys.path.insert(0, '../S184_大人がさっきいたか_20261121')
from multiprocessing import Pool
腕 = {'なし': (None, '両方'), '両方': (0.5, '両方'), '顔だけ': (0.5, '顔だけ'), '手だけ': (0.5, '手だけ')}
def one(job):
    import 数え; s, 名, L = job; return 数え.長く(s, *腕[名], 寿命=L, 気づく=True)[:3]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for L in [8000, 24000]:
            R = {名: np.array(p.map(one, [(s, 名, L) for s in range(900, 906)], chunksize=1)) for 名 in 腕}
            for 名, r in R.items():
                m = np.median(r, 0); print(f'寿命{L} {名}: 終わりの指す差 {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/6） 取る差 {m[1]:+.3f} 食べ {m[2]:.4f}', flush=True)
            print(f'寿命{L} 顔だけ>手だけ（指す差）: {int((R["顔だけ"][:,0] > R["手だけ"][:,0]).sum())}/6', flush=True)

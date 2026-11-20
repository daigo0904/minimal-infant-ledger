import sys, numpy as np
sys.path.insert(0, '../S174_親のそばは損が小さい_20261120')
from multiprocessing import Pool
from 数え import 測る
def one(job): return 測る(*job)[:13]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for 守, 見 in [(None, True), (0.2, True), (0.0, True), (None, False), (0.2, False)]:
            r = np.array(p.map(one, [(s, 'v4', 守, 見) for s in range(900, 910)], chunksize=1)); m = np.median(r, 0)
            print(f'守り{守} 見たら次は養育者{見}: 分からない物 取る差 {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） 見る差 {m[1]:+.3f}（>0 {int((r[:,1]>0).sum())}/10） ／ あり 取る差 {m[2]:+.3f} ／ 分からない物 取る 養育者 {m[4]:.3f} 仲間 {m[6]:.3f} 食べ {m[12]:.4f}', flush=True)

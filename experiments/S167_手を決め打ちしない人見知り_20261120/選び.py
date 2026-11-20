import sys, numpy as np
sys.path.insert(0, '../S167_手を決め打ちしない人見知り_20261120')
from multiprocessing import Pool
from 共 import *
def one(job):
    s, k, 型 = job; o = 一生(s, '見る', 'v4', 知らない=(4000, 0.3), kU=k, kU型=型); x = 人見(o, 4000, 5000); y = 人見(o, 7000, 8000)
    return ((x[0] + x[2]) / 2 - (x[4] + x[6]) / 2, (x[1] + x[3]) / 2 - (x[5] + x[7]) / 2, (y[0] + y[2]) / 2 - (y[4] + y[6]) / 2, 数える(o, 7000, 8000)[0], float(o['食列'][6000:].mean()))
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for k, 型 in [(0.0, '手0'), (0.2, '手0'), (0.2, '全手'), (0.5, '全手'), (1.0, '全手')]:
            r = np.array(p.map(one, [(s, k, 型) for s in range(900, 910)], chunksize=1)); m = np.median(r, 0)
            print(f'{型} kU{k}: 会い始め 取る差 {m[0]:+.3f}（<0 {int((r[:,0]<0).sum())}/10） 顔を見る差 {m[1]:+.3f}（>0 {int((r[:,1]>0).sum())}/10） 慣れた後 取る差 {m[2]:+.3f} 情報探し {m[3]:+.3f}（{int((r[:,3]>0).sum())}/10） 食べ {m[4]:.4f}', flush=True)

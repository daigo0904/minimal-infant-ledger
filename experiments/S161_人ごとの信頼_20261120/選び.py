import sys, numpy as np
sys.path.insert(0, '../S161_人ごとの信頼_20261120')
from multiprocessing import Pool
from 共 import *
G2 = (4000, 0.9)
def one(job):
    s, 正直, k = job; o = 一生(s, '養育者', 物知り=(1, 正直), 合図2=G2, kτ=k)
    return (数える(o, s, (1, 正直), 3000, 4000)[1], 合図2の差(o, s, G2, 4000, 5000), 合図2の差(o, s, G2, 7000, 8000), float(o['食列'].mean()))
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for k in [0.0, 10.0, 50.0, 200.0]:
            r = {正直: np.array(p.map(one, [(s, 正直, k) for s in range(900, 910)], chunksize=1)) for 正直 in [1.0, 0.5]}
            m1, m5 = np.median(r[1.0], 0), np.median(r[0.5], 0)
            print(f'kτ{k}: 前半終わり表情 {m1[0]:+.3f}/{m5[0]:+.3f} 後半初め合図2 {m1[1]:+.3f}/{m5[1]:+.3f}（1.0>0.5 {int((r[1.0][:,1] > r[0.5][:,1]).sum())}/10） 後半終わり {m1[2]:+.3f}/{m5[2]:+.3f} 食べ {m1[3]:.4f}', flush=True)

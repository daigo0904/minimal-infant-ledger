import sys, numpy as np
sys.path.insert(0, '../S162_人ごとの信頼を直す_20261120')
from multiprocessing import Pool
from 共 import *
G2 = (4000, 0.9)
def one(job):
    s, 正直, k = job; o = 一生(s, '養育者', 物知り=(1, 正直), 合図2=G2, kτ=k, 物知り率=0.5, 信型='一致')
    return (数える(o, s, (1, 正直), 3000, 4000)[1], 合図2の差(o, s, G2, 4000, 4500), 合図2の差(o, s, G2, 4000, 5000), 合図2の差(o, s, G2, 7000, 8000), float(o['食列'].mean()))
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for k in [0.0, 50.0, 150.0, 400.0]:
            r = {正直: np.array(p.map(one, [(s, 正直, k) for s in range(900, 910)], chunksize=1)) for 正直 in [1.0, 0.5]}
            m1, m5 = np.median(r[1.0], 0), np.median(r[0.5], 0)
            print(f'kτ{k}: 前半終わり表情 {m1[0]:+.3f}/{m5[0]:+.3f} 合図2 4000-4500 {m1[1]:+.3f}/{m5[1]:+.3f}（{int((r[1.0][:,1] > r[0.5][:,1]).sum())}/10） 4000-5000 {m1[2]:+.3f}/{m5[2]:+.3f}（{int((r[1.0][:,2] > r[0.5][:,2]).sum())}/10） 7000-8000 {m1[3]:+.3f}/{m5[3]:+.3f} 食べ {m1[4]:.4f}', flush=True)

import sys, numpy as np
sys.path.insert(0, '../S133_相手ごとの足りなさ_20261119')
from multiprocessing import Pool
from 共 import *
if __name__ == '__main__':
    with Pool(8) as p:
        for kD in [0.0, 10.0, 30.0, 100.0]:
            r = np.array(p.map(one, [(s, kD) for s in range(900, 910)])); m = np.median(r, 0)
            print(f'kD={kD}: 親友が戻った後の増え 親友の前で親友の手 {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） 養育者の前で一番 {m[1]:+.3f}（>0 {int((r[:,1]>0).sum())}/10） | 不在なし 親友 {m[2]:.3f} 養 {m[3]:.3f}')

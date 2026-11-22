import numpy as np
from multiprocessing import Pool
from 共 import *
if __name__ == '__main__':
    with Pool(8) as p:
        for kD in [0.0, 30.0]:
            r = np.array(p.map(one, [(s, kD) for s in range(900, 910)])); m = np.median(r, 0)
            print(f'kD={kD}: 増え 250手 {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） 500手 {m[1]:+.3f}（{int((r[:,1]>0).sum())}/10） 1000手 {m[2]:+.3f}（{int((r[:,2]>0).sum())}/10）  1000>250 {int((r[:,2]>r[:,0]).sum())}/10')

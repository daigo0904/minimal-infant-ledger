import sys, numpy as np
sys.path.insert(0, '../S135_順番交代_20261119')
from multiprocessing import Pool
from 共 import *
def one(job): s, 番 = job; o = 一生(s, 番); return 数える(o, 0, 1000) + 数える(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8) as p:
        for 番 in ['交代', 'でたらめ']:
            r = np.array(p.map(one, [(s, 番) for s in range(900, 910)])); m = np.median(r, 0)
            print(f'{番}: 初め 聞く時に声 {m[0]:.3f} 話す時に声 {m[1]:.3f} 差 {m[2]:+.3f} | 終わり {m[4]:.3f} {m[5]:.3f} 差 {m[6]:+.3f}（育つ {int((r[:,6] > r[:,2]).sum())}/10） 食べ {m[7]:.4f}')

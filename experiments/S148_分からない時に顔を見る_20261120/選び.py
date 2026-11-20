import sys, numpy as np
sys.path.insert(0, '../S148_分からない時に顔を見る_20261120')
from multiprocessing import Pool
from 共 import *
def one(job): s, 名 = job; o = 一生(s, '見る', 名); return 数える(o, 0, 1000) + 数える(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8) as p:
        for 名 in ['元', 'v3']:
            r = np.array(p.map(one, [(s, 名) for s in range(900, 910)])); m = np.median(r, 0)
            print(f'{名}: 分からない時に顔を見る − 分かる時 初め {m[0]:+.3f} 終わり {m[5]:+.3f}（>0 {int((r[:,5] > 0).sum())}/10）（見る 無 {m[6]:.3f} 有 {m[7]:.3f}） | 見えた表情に従う {m[8]:+.3f} | 食べ {m[9]:.4f}')

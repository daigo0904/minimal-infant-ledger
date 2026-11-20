import sys, numpy as np
sys.path.insert(0, '../S147_社会的参照_20261120')
from multiprocessing import Pool
from 共 import *
def one(job): s, 参照, 名 = job; o = 一生(s, 参照, 名); return 数える(o, 0, 1000) + 数える(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8) as p:
        for 名 in ['元', 'v3']:
            for 参照 in ['養育者', 'ずらし']:
                r = np.array(p.map(one, [(s, 参照, 名) for s in range(900, 910)])); m = np.median(r, 0)
                print(f'{名} {参照}: 養育者の表情に従う差 初め {m[0]:+.3f} 終わり {m[4]:+.3f}（育つ {int((r[:,4] > r[:,0]).sum())}/10） | 仲間の表情に従う差 {m[5]:+.3f} | 食べ {m[7]:.4f}')

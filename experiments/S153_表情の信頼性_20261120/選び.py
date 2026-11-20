import sys, numpy as np
sys.path.insert(0, '../S153_表情の信頼性_20261120')
from multiprocessing import Pool
from 共 import *
def one(job): s, 正直 = job; o = 一生(s, '養育者', 'v4', 物知り=(1, 正直)); return 数える(o, 0, 2000) + 数える(o, 6000, 8000)
if __name__ == '__main__':
    with Pool(8) as p:
        rs = {}
        for 正直 in [1.0, 0.7, 0.5]:
            r = np.array(p.map(one, [(s, 正直) for s in range(900, 910)])); rs[正直] = r; m = np.median(r, 0)
            print(f'物知りの正直さ {正直}: 表情に従う差 終わり 養育者 {m[4]:+.3f} 物知り {m[5]:+.3f} ほかの仲間 {m[6]:+.3f}（初め 物知り {m[1]:+.3f}） 食べ {m[7]:.4f}')
        print('物知り 1.0 > 0.7 の世界:', int((rs[1.0][:, 5] > rs[0.7][:, 5]).sum()), '/10   0.7 > ほかの仲間:', int((rs[0.7][:, 5] > rs[0.7][:, 6]).sum()), '/10')

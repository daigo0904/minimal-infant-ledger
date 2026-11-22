import sys, numpy as np
sys.path.insert(0, '../S155_物知りに会う回数_20261120')
from multiprocessing import Pool
from 共 import *
def one(job): s, 率, 正直 = job; o = 一生(s, '養育者', 'v4', 物知り=(1, 正直), 物知り率=率); return 数える(o, 0, 2000) + 数える(o, 6000, 8000)
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        rs = {}
        for 率 in [None, 0.5]:
            for 正直 in [1.0, 0.7, 0.5]:
                r = np.array(p.map(one, [(s, 率, 正直) for s in range(900, 910)], chunksize=1)); rs[(率, 正直)] = r; m = np.median(r, 0)
                print(f'率{率} 正直さ{正直}: 終わり 養育者 {m[4]:+.3f} 物知り {m[5]:+.3f} ほか {m[6]:+.3f}（初め 物知り {m[1]:+.3f}） 食べ {m[7]:.4f}', flush=True)
        print('0.7物知り 率0.5>そのまま:', int((rs[(0.5, 0.7)][:, 5] > rs[(None, 0.7)][:, 5]).sum()), '/10')
        print('1.0物知り 率0.5>そのまま:', int((rs[(0.5, 1.0)][:, 5] > rs[(None, 1.0)][:, 5]).sum()), '/10')
        print('率0.5 0.7>0.5:', int((rs[(0.5, 0.7)][:, 5] > rs[(0.5, 0.5)][:, 5]).sum()), '/10')
        print('率0.5 0.7物知り/1.0物知り 比:', round(float(np.median(rs[(0.5, 0.7)][:, 5]) / np.median(rs[(0.5, 1.0)][:, 5])), 3), ' そのまま:', round(float(np.median(rs[(None, 0.7)][:, 5]) / np.median(rs[(None, 1.0)][:, 5])), 3))

import sys, numpy as np
sys.path.insert(0, '../S175_相手ごとの好み_20261120')
from multiprocessing import Pool
from 共 import *
def one(s): o = 一生(s, 'v4', 二人=0.5, B同じ=True); return 分け(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: r = np.array(p.map(one, range(900, 910)))
    print('B同じ好み・v4 終わり 人ごとの見られ分け', round(float(np.median(r)), 3), ' 範囲', round(float(r.min()), 3), round(float(r.max()), 3))

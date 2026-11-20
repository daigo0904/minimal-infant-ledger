import sys, numpy as np
sys.path.insert(0, '../S175_相手ごとの好み_20261120')
from multiprocessing import Pool
from 共 import *
def one(job): s, 名 = job; o = 一生(s, 名, 二人=0.5); return 分け(o, 0, 1000), 分け(o, 7000, 8000), float(o['食列'][7000:].mean())
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)) for 名 in ['元', 'v4']}
    for 名, r in R.items():
        m = np.median(r, 0); print(f'{名}: 人ごとの見られ分け 初め {m[0]:+.3f} 終わり {m[1]:+.3f}（>0 {int((r[:,1]>0).sum())}/10、終わり>初め {int((r[:,1]>r[:,0]).sum())}/10） 食べ {m[2]:.4f}')
    print('v4 > 元（終わり）:', int((R['v4'][:, 1] > R['元'][:, 1]).sum()), '/10')

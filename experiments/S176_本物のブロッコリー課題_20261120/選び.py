import sys, numpy as np
sys.path.insert(0, '../S176_本物のブロッコリー課題_20261120')
from multiprocessing import Pool
from 共 import *
def one(job): s, 名, x = job; o = 一生(s, 名, 二人=0.5, 自分=x); return ブロッコリー(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for x in [0.02, 0.05, 0.1, 0.2]:
            for 名 in ['元', 'v4']:
                r = np.array(p.map(one, [(s, 名, x) for s in range(900, 910)], chunksize=1)); m = np.median(r, 0)
                print(f'自分{x} {名}: B の前 B好き−自分好き {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） 仲間の前の自分好き {m[1]:.3f} A の前 A好き−自分好き {m[2]:+.3f}', flush=True)

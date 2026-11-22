import sys, numpy as np
sys.path.insert(0, '../S160_信頼の持ち越し_20261120')
from multiprocessing import Pool
from 共 import *
G2 = (4000, 0.9)
def one(job):
    s, 正直 = job; o = 一生(s, '養育者', 物知り=(1, 正直), 合図2=G2)
    return (数える(o, s, (1, 正直), 3000, 4000)[1], 合図2の差(o, s, G2, 4000, 4500), 合図2の差(o, s, G2, 4000, 5000), 合図2の差(o, s, G2, 7000, 8000), 合図2の差(o, s, G2, 4000, 5000, 3))
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: r = {正直: np.array(p.map(one, [(s, 正直) for s in range(900, 910)], chunksize=1)) for 正直 in [1.0, 0.5]}
    for 正直 in r:
        m = np.median(r[正直], 0); print(f'表情の正直さ{正直}: 前半の終わり 表情に従う {m[0]:+.3f} ／ 後半 合図2に従う 4000-4500 {m[1]:+.3f} 4000-5000 {m[2]:+.3f} 7000-8000 {m[3]:+.3f} ／ 対照(ほかの仲間 3の前) {m[4]:+.3f}')
    for j, n in [(1, '4000-4500'), (2, '4000-5000'), (3, '7000-8000')]: print(n, '1.0>0.5:', int((r[1.0][:, j] > r[0.5][:, j]).sum()), '/10')

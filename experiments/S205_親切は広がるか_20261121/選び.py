import sys, numpy as np
sys.path.insert(0, '../S205_親切は広がるか_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:2]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in [1.0, 0.0]}
    for k, r in R.items(): print(f'kG{k}: 終わりの親切な子の数 中央値 {np.median(r[:,0]):.1f}（はじめ 4、>4 {int((r[:,0]>4).sum())}/10、<4 {int((r[:,0]<4).sum())}/10） 各世界 {r[:,0].tolist()}')
    print('kG1 > kG0:', int((R[1.0][:,0] > R[0.0][:,0]).sum()), '/10')

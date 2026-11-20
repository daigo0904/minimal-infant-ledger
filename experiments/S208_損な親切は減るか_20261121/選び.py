import sys, numpy as np
sys.path.insert(0, '../S208_損な親切は減るか_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:2]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in [0.0, 1.0]}
    for k, r in R.items(): print(f'kG{k}: 終わりの親切数 中央値 {np.median(r[:,0]):.2f}（<4 {int((r[:,0]<4).sum())}/10） 中ほど {np.median(r[:,1]):.2f}  各 {np.round(r[:,0], 1).tolist()}')
    print('kG1 > kG0:', int((R[1.0][:,0] > R[0.0][:,0]).sum()), '/10')

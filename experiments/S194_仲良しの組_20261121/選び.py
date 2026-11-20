import sys, numpy as np
sys.path.insert(0, '../S194_仲良しの組_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:2]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in [0.0, 1.0, 3.0]}
    for k, r in R.items(): m = np.median(r, 0); print(f'kG{k}: 組のそろい方（相関）{m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） なぐさめ先の偏り（上位2人）{m[1]:.3f}（偶然 0.286）')
    for k in [1.0, 3.0]: print(f'kG{k} > kG0：相関 {int((R[k][:,0] > R[0.0][:,0]).sum())}/10 偏り {int((R[k][:,1] > R[0.0][:,1]).sum())}/10')

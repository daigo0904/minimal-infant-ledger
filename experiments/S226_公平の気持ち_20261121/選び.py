import sys, numpy as np
sys.path.insert(0, '../S226_公平の気持ち_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return 数え.測る(s, k)[:4]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in [0.0, 1.0, 5.0, 20.0]}
    for k, r in R.items(): print(f'kQ{k}: 少ない−多い 中央値 {np.median(r[:,0]):+.4f}（>0 {int((r[:,0]>0).sum())}/10）・受けた量の変動係数 {np.median(r[:,1]):.3f}・空腹のばらつき {np.median(r[:,2]):.4f}・なぐさめ {np.median(r[:,3]):.3f}', flush=True)
    z = R[0.0]
    for k in [1.0, 5.0, 20.0]: a = R[k]; print(f'kQ{k}: 差>kQ0 {int((a[:,0] > z[:,0]).sum())}/10・変動係数<kQ0 {int((a[:,1] < z[:,1]).sum())}/10・空腹のばらつき<kQ0 {int((a[:,2] < z[:,2]).sum())}/10')

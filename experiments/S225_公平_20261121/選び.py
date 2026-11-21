import sys, numpy as np
sys.path.insert(0, '../S225_公平_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, v = job; return 数え.測る(s, v)[:3]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {v: np.array(p.map(one, [(s, v) for s in range(900, 910)], chunksize=1)) for v in [True, False]}
    for v, r in R.items(): print(f'公平入力={v}: 少ない−多い {np.round(r[:,0], 3).tolist()} 中央値 {np.median(r[:,0]):+.4f}（>0 {int((r[:,0]>0).sum())}/10）・空腹 高い−低い {np.median(r[:,1]):+.4f}・なぐさめ {np.median(r[:,2]):.3f}', flush=True)
    print(f'入力あり>なし {int((R[True][:,0] > R[False][:,0]).sum())}/10')

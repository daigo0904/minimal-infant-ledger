import sys, numpy as np
sys.path.insert(0, '../S243_共感の見込み_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, k, c = job; return 数え.測る(s, k, c)[:3]
if __name__ == '__main__':
    J = [(s, k, c) for c in [False, True] for k in [0.0, 3.0, 10.0] for s in range(900, 910)]
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, J, chunksize=1)
    R = {}
    for (s, k, c), v in zip(J, r): R.setdefault((k, c), []).append(v)
    R = {key: np.array(v) for key, v in R.items()}
    for (k, c), v in R.items(): print(f"{'競う' if c else '協力'} kC{k}: 当たり 中央値 {np.median(v[:,0]):.3f}（{np.round(v[:,0].min(),3)}〜{np.round(v[:,0].max(),3)}）・全体 {np.median(v[:,1]):.3f}・話し手ごと {np.median(v[:,2]):.3f}", flush=True)
    print(f"協力 kC10>kC0 {int((R[(10.0, False)][:,0] > R[(0.0, False)][:,0]).sum())}/10・競う kC10>kC0 {int((R[(10.0, True)][:,0] > R[(0.0, True)][:,0]).sum())}/10・競う kC10>0.30 {int((R[(10.0, True)][:,0] > 0.30).sum())}/10・競う kC3>0.30 {int((R[(3.0, True)][:,0] > 0.30).sum())}/10")

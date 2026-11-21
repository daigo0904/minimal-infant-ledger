import sys, numpy as np
sys.path.insert(0, '../S240_強い共感_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return 数え.測る(s, k)[:3]
if __name__ == '__main__':
    K = [0.0, 50.0, 200.0, 500.0]
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in K}
    for k, r in R.items(): print(f'kE{k}: 当たり {np.round(r[:,0],3).tolist()} 中央値 {np.median(r[:,0]):.3f}・全体 {np.median(r[:,1]):.3f}・話し手ごと {np.median(r[:,2]):.3f}', flush=True)
    print(f'当たり kE500>kE50 {int((R[500.0][:,0] > R[50.0][:,0]).sum())}/10・kE500>0.30 {int((R[500.0][:,0] > 0.30).sum())}/10・kE50>kE0 {int((R[50.0][:,0] > R[0.0][:,0]).sum())}/10・kE200>kE50 {int((R[200.0][:,0] > R[50.0][:,0]).sum())}/10')

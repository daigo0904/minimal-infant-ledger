import sys, numpy as np
sys.path.insert(0, '../S238_得がぶつかる世界_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return 数え.測る(s, k)[:3]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in [False, True]}
    for k, r in R.items(): print(f'競う={k}: 当たり {np.round(r[:,0],3).tolist()} 中央値 {np.median(r[:,0]):.3f}・全体 {np.median(r[:,1]):.3f}・話し手ごと {np.median(r[:,2]):.3f}', flush=True)
    a, b = R[True], R[False]; print(f'当たり 競う<協力 {int((a[:,0] < b[:,0]).sum())}/10・競う<0.25 {int((a[:,0] < 0.25).sum())}/10・話し手ごと 競う<協力 {int((a[:,2] < b[:,2]).sum())}/10・全体 競う<協力 {int((a[:,1] < b[:,1]).sum())}/10')

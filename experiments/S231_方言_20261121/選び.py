import sys, numpy as np
sys.path.insert(0, '../S231_方言_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, m = job; return 数え.測る(s, m)[:4]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {m: np.array(p.map(one, [(s, m) for s in range(900, 910)], chunksize=1)) for m in [0.02, 0.5]}
    for m, r in R.items(): print(f'm{m}: 群れの中の一致 {np.median(r[:,0]):.3f}・群れどうし {np.round(r[:,1],2).tolist()} 中央値 {np.median(r[:,1]):.3f}・当たり 中 {np.median(r[:,2]):.3f} またぐ {np.median(r[:,3]):.3f}', flush=True)
    a, b = R[0.02], R[0.5]; print(f'm0.02：どうし<中 {int((a[:,1] < a[:,0]).sum())}/10・どうし m0.02<m0.5 {int((a[:,1] < b[:,1]).sum())}/10・またぐ当たり<中 {int((a[:,3] < a[:,2]).sum())}/10')

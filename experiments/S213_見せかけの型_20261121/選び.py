import sys, numpy as np
sys.path.insert(0, '../S213_見せかけの型_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, 見評 = job; return 数え.測る(s, 見評=見評)[:2]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {v: np.array(p.map(one, [(s, v) for s in range(900, 910)], chunksize=1)) for v in [True, False]}
    for v, r in R.items(): d = r[:,1] - r[:,0]; print(f'見られ評判={v}: いつも {np.round(r[:,0],1).tolist()} 見せ {np.round(r[:,1],1).tolist()}・差（見せ−いつも）中央値 {np.median(d):+.2f}（>0 {int((d>0).sum())}/10・<0 {int((d<0).sum())}/10）・親切計 中央値 {np.median(r.sum(1)):.2f}', flush=True)
    a, b = R[True], R[False]; print(f'見せ−いつも 見られ評判 > いつも評判 {int(((a[:,1]-a[:,0]) > (b[:,1]-b[:,0])).sum())}/10')

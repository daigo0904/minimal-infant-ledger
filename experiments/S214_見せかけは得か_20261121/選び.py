import sys, numpy as np
sys.path.insert(0, '../S214_見せかけは得か_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, v = job; return 数え.測る(s, 見評=v)[:4]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {v: np.array(p.map(one, [(s, v) for s in range(900, 910)], chunksize=1)) for v in [True, False]}
    for v, r in R.items(): print(f'見られ評判={v}: 差（見せ−いつも）{np.round(r[:,0], 4).tolist()} 中央値 {np.median(r[:,0]):+.4f}（<0 {int((r[:,0]<0).sum())}/10）・空腹 見せ {np.median(r[:,1]):.4f} いつも {np.median(r[:,2]):.4f} 親切でない {np.median(r[:,3]):.4f}', flush=True)
    print(f'見られ評判の差 < いつも評判の差 {int((R[True][:,0] < R[False][:,0]).sum())}/10')

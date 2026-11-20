import sys, numpy as np
sys.path.insert(0, '../S204_親切の見返り_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:5]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in [1.0, 3.0]}
    for k, r in R.items(): m = np.median(r, 0); print(f'親切{k}（子0〜3 − 子4〜7）: なぐさめてもらった {m[0]:+.0f}（>0 {int((r[:,0]>0).sum())}） 入り次数 {m[1]:+.2f}（>0 {int((r[:,1]>0).sum())}） 空腹 {m[2]:+.3f}（<0 {int((r[:,2]<0).sum())}） 食べ {m[3]:+.4f}（>0 {int((r[:,3]>0).sum())}） なぐさめた {m[4]:+.3f}')

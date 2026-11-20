import sys, numpy as np
sys.path.insert(0, '../S201_転入生を何度も_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:2]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {γ: np.array(p.map(one, [(s, γ) for s in range(900, 910)], chunksize=1)) for γ in [0.0, 5.0]}
    for γ, r in R.items(): m = np.median(r, 0); print(f'γ{γ}: 転入生 − 古株 なぐさめてもらった {m[0]:+.1f}（<0 {int((r[:,0]<0).sum())}/10） 入り次数 {m[1]:+.2f}（<0 {int((r[:,1]<0).sum())}/10）')
    print('γ5 で不利が小さい：なぐさめ', int((R[5.0][:,0] > R[0.0][:,0]).sum()), '/10 入り次数', int((R[5.0][:,1] > R[0.0][:,1]).sum()), '/10')

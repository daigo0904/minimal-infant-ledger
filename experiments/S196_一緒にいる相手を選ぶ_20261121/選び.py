import sys, numpy as np
sys.path.insert(0, '../S196_一緒にいる相手を選ぶ_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:3]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {β: np.array(p.map(one, [(s, β) for s in range(900, 910)], chunksize=1)) for β in [0.0, 0.3, 0.5, 1.0]}
    for β, r in R.items(): m = np.nanmedian(r, 0); print(f'β{β}: 相関 {m[0]:+.3f} なぐさめ先の偏り {m[1]:.3f} 会う偏り {m[2]:.3f}（偶然 0.286）')
    for β in [0.3, 0.5, 1.0]: print(f'β{β} > β0：なぐさめ先の偏り {int((R[β][:,1] > R[0.0][:,1]).sum())}/10 会う偏り {int((R[β][:,2] > R[0.0][:,2]).sum())}/10 相関 {int((R[β][:,0] > R[0.0][:,0]).sum())}/10')

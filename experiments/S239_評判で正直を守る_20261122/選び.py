import sys, numpy as np
sys.path.insert(0, '../S239_評判で正直を守る_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, ρ = job; return 数え.測る(s, ρ)[:3]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {ρ: np.array(p.map(one, [(s, ρ) for s in range(900, 910)], chunksize=1)) for ρ in [0.0, 5.0, 10.0]}
    for ρ, r in R.items(): print(f'ρ{ρ}: 当たり {np.round(r[:,0],3).tolist()} 中央値 {np.median(r[:,0]):.3f}・全体 {np.median(r[:,1]):.3f}・話し手ごと {np.median(r[:,2]):.3f}', flush=True)
    for ρ in [5.0, 10.0]: a, z = R[ρ], R[0.0]; print(f'ρ{ρ}：当たり>ρ0 {int((a[:,0] > z[:,0]).sum())}/10・>0.30 {int((a[:,0] > 0.30).sum())}/10・全体>ρ0 {int((a[:,1] > z[:,1]).sum())}/10')

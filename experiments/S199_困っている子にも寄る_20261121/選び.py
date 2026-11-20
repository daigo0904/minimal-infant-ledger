import sys, numpy as np
sys.path.insert(0, '../S199_困っている子にも寄る_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:6]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {γ: np.array(p.map(one, [(s, γ) for s in range(900, 910)], chunksize=1), dtype=float) for γ in [0.0, 2.0, 5.0]}
    for γ, r in R.items(): m = np.nanmedian(r, 0); print(f'γ{γ}: 外れの空腹差 {m[0]:+.3f} なぐさめてもらった差 {m[1]:+.0f} 会う偏り {m[2]:.3f} 両思い {m[3]:.3f} 全体の空腹 {m[4]:.3f} 外れの数 {m[5]:.1f}')
    for γ in [2.0, 5.0]: a, b = R[γ], R[0.0]; print(f'γ{γ} vs γ0：空腹差が小さい {int((np.nan_to_num(a[:,0], nan=-9) < np.nan_to_num(b[:,0], nan=9)).sum())}/10 会う偏りが小さい {int((a[:,2] < b[:,2]).sum())}/10 両思いが小さい {int((a[:,3] < b[:,3]).sum())}/10 全体の空腹が低い {int((a[:,4] < b[:,4]).sum())}/10')

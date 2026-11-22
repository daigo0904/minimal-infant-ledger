import sys, numpy as np
sys.path.insert(0, '../S182_長く育てる_20261120')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:6]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {α: np.array(p.map(one, [(s, α) for s in range(900, 906)], chunksize=1)) for α in [None, 0.5]}
    for α, r in R.items():
        m = np.median(r, 0); print(f'記憶{α}: 6000-8000 指す差 {m[0]:+.3f} 取る差 {m[1]:+.3f} 食べ {m[2]:.4f} ／ 22000-24000 指す差 {m[3]:+.3f}（>0 {int((r[:,3]>0).sum())}/6） 取る差 {m[4]:+.3f} 食べ {m[5]:.4f}')
    print('終わりの食べ 記憶>なし:', int((R[0.5][:, 5] > R[None][:, 5]).sum()), '/6  指す差が育つ（終わり>6000-8000）:', int((R[0.5][:, 3] > R[0.5][:, 0]).sum()), '/6')

"""u=φᵀP0φ の大きさ：知らない大人の前（会い始め）と仲間・養育者の前。kU=0 の v4。"""
import sys, numpy as np
sys.path.insert(0, '../S165_見慣れなさは分からなさ_20261120')
from multiprocessing import Pool
import 共 as C
皆 = []
class 診(C.包):
    def __init__(s, *a): super().__init__(*a); s.ul = []; 皆.append(s)
    def 選ぶ(s, φ): s.ul.append(float(φ @ s.食[0].P @ φ)); return super().選ぶ(φ)
def one(s):
    C.包 = 診; o = C.一生(s, '見る', 'v4', 知らない=(4000, 0.3)); U = np.array([c.ul for c in 皆]).T; 相 = o['相手列']; r = []
    for lo, hi in [(3500, 4000), (4000, 4500), (7000, 8000)]:
        u, a = U[lo:hi], 相[lo:hi]; r += [float(u[a == 0].mean()), float(u[(a > 0) & (a < 9)].mean()), float(u[a == 9].mean()) if (a == 9).any() else np.nan]
    return r
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: r = np.array(p.map(one, range(900, 908), chunksize=1))
    m = np.nanmedian(r, 0); print(f'u 3500-4000 養育者 {m[0]:.4f} 仲間 {m[1]:.4f} ／ 4000-4500 養育者 {m[3]:.4f} 仲間 {m[4]:.4f} 知らない {m[5]:.4f} ／ 7000-8000 養育者 {m[6]:.4f} 仲間 {m[7]:.4f} 知らない {m[8]:.4f}')
    print('会い始め 知らない>仲間:', int((r[:, 5] > r[:, 4]).sum()), '/8')

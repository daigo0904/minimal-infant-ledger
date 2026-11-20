import sys, numpy as np
sys.path.insert(0, '../S162_人ごとの信頼を直す_20261120')
from multiprocessing import Pool
import 共
class 診(共.包):
    def __init__(s, *a): super().__init__(*a); s.記 = []; 共.皆.append(s)
    def 選ぶ(s, φ): s.記.append((s.信.予測(s.感覚(s.顔見)), 0.0, 0.0)); return super().選ぶ(φ)
共.記包 = 診
def one(job):
    s, 正直, k = job; o = 共.一生(s, '養育者', 物知り=(1, 正直), 合図2=(4000, 0.9), kτ=k, 物知り率=0.5, 記録=True, 信型=sys.argv[2] if len(sys.argv) > 2 else '外れ'); τ = o['記'][:, :, 0]; 相 = o['相手列']; r = []
    for lo, hi in [(3000, 4000), (4000, 4500)]:
        T, A = τ[lo:hi], 相[lo:hi]; r += [float(T[A == 0].mean()), float(T[A == 2].mean()), float(T[(A > 0) & (A != 2)].mean())]
    return r
if __name__ == '__main__':
    k = float(sys.argv[1])
    with Pool(8, maxtasksperchild=1) as p:
        R = {正直: np.array(p.map(one, [(s, 正直, k) for s in range(900, 910)], chunksize=1)) for 正直 in [1.0, 0.5]}
    for 正直, r in R.items():
        m = np.median(r, 0); print(f'kτ{k} 正直{正直}: τ 3000-4000 養育者 {m[0]:+.4f} 物知り {m[1]:+.4f} ほか {m[2]:+.4f} ／ 4000-4500 養育者 {m[3]:+.4f} 物知り {m[4]:+.4f} ほか {m[5]:+.4f}')
    print('物知りの τ 1.0>0.5（3000-4000）:', int((R[1.0][:, 1] > R[0.5][:, 1]).sum()), '/10  （4000-4500）:', int((R[1.0][:, 4] > R[0.5][:, 4]).sum()), '/10  1.0で物知り>ほか:', int((R[1.0][:, 1] > R[1.0][:, 2]).sum()), '/10')

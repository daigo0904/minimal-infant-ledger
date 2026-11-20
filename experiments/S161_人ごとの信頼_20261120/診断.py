"""τ が相手ごとにどう違うか（3000〜4000手・後半 4000〜4500）。乱数を使わない記録だけ。"""
import sys, numpy as np
sys.path.insert(0, '../S161_人ごとの信頼_20261120')
from multiprocessing import Pool
import 共
class 診(共.包):
    def __init__(s, *a): super().__init__(*a); s.記 = []; 共.皆.append(s)
    def 選ぶ(s, φ): s.記.append((s.信.予測(φ), s.信平均 or 0.0, 0.0)); return super().選ぶ(φ)
共.記包 = 診
def one(job):
    s, 正直 = job; o = 共.一生(s, '養育者', 物知り=(1, 正直), 合図2=(4000, 0.9), kτ=10.0, 記録=True); τ = o['記'][:, :, 0]; 相 = o['相手列']; r = []
    for lo, hi in [(3000, 4000), (4000, 4500)]:
        T, A = τ[lo:hi], 相[lo:hi]; r += [float(T[A == 0].mean()), float(T[A == 2].mean()), float(T[(A > 0) & (A != 2)].mean())]
    return r + [float(o['記'][3999, :, 1].mean())]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for 正直 in [1.0, 0.5]:
            m = np.median(np.array(p.map(one, [(s, 正直) for s in range(900, 908)], chunksize=1)), 0)
            print(f'正直{正直}: τ 3000-4000 養育者 {m[0]:+.4f} 物知り {m[1]:+.4f} ほか {m[2]:+.4f} ／ 4000-4500 養育者 {m[3]:+.4f} 物知り {m[4]:+.4f} ほか {m[5]:+.4f} ／ 外れの平均 {m[6]:.4f}')

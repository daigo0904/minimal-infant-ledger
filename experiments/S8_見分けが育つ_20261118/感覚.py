"""S8 の感覚：見た目の「型」を K 個持ち、近さを感覚にする。育つ型は経験で型を見た目に寄せる（競合学習）。固定の型は学ばない。"""
import numpy as np
K = 16
温度 = 0.5
学び始め = 0.05
学び時定数 = 2000.0
class 型の感覚:
    def __init__(self, rng, 育つ, 次元=8):
        self.型 = rng.normal(0, 1, (K, 次元)); self.育つ = 育つ; self.回 = 0
    def __call__(self, v):
        d = ((self.型 - v) ** 2).sum(axis=1)
        w = np.exp(-(d - d.min()) / (2 * 温度 ** 2 * 8)); w /= w.sum()
        if self.育つ:
            j = int(np.argmin(d)); η = 学び始め / (1 + self.回 / 学び時定数); self.型[j] += η * (v - self.型[j]); self.回 += 1
        return np.append(w, 1.0)

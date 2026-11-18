import sys, numpy as np
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # S30：換算型（c=30）と S16 世界（感覚256・雑音0.3）
W = B.W
m時定数 = 1000.0
class 合図(B.換算):
    """Q の入力に「この相手は大事か」z = u / (|u| のゆっくりした平均) を1つ足す（±3 で切る）。評価とつながりは元の φ のまま"""
    def __init__(s, 種, i, 頭):
        super().__init__(種, i, 頭); s.Q = np.zeros((W.行動数, W.感覚数 + 2)); s.m = 0.0; s.拡 = None
    def 選ぶ(s, φ):
        u = s.つながり.予測(φ); s.m += (abs(u) - s.m) / m時定数
        z = float(np.clip(u / (s.m + 1e-3), -3, 3)); s.拡 = np.append(φ, z)
        q = s.Q @ s.拡
        ê = np.array([m.予測(φ) for m in s.評価])
        score = q + B.c * max(s.v食, 0.0) * u * ê
        a = int(np.argmax(score))
        if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
        return a, q, ê
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        super().受ける(φ, a, q, e, 食べた, 我慢); _, a2, R = s.前; s.前 = (s.拡, a2, R)
def 一生(s, 合図あり, 寿命=8000):
    W.赤ちゃん = 合図 if 合図あり else B.換算
    try: return W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.赤ちゃん = B.原
def one(job):
    s, k = job; o = 一生(s, k); return (s, k, B.区(o, 0, 500), [float(np.mean([B.区(o, 7000, 7500)[j], B.区(o, 7500, 8000)[j]])) for j in range(3)])

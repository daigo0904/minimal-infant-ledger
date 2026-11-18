import sys, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
原 = W.赤ちゃん
歩幅 = [0.01]
class LMS:
    """遅い学び：w += 歩幅·(y − w·φ)·φ/|φ|²（RLS は P初め10 で数百手で学び終わる）"""
    def __init__(s, n): s.w = np.zeros(n)
    def 予測(s, φ): return float(s.w @ φ)
    def 学ぶ(s, φ, y):
        n2 = φ @ φ
        if n2 > 0: s.w += 歩幅[0] * (y - s.w @ φ) * φ / n2
class 遅い(原):
    def __init__(s, 種, i, 頭):
        super().__init__(種, i, 頭); s.つながり = LMS(W.感覚数 + 1)
def 一生(種, 頭, 遅く=False, 寿命=8000):
    W.赤ちゃん = 遅い if 遅く else 原
    try: return W.一生(種, '依存', 頭, 寿命=寿命, 離乳=寿命)
    finally: W.赤ちゃん = 原
def 数字(o):
    _, _, 差 = W.区間の数字(o); return 差[0], float(np.mean(差[14:16])), 差

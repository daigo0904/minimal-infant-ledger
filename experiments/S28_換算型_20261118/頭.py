import sys, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
原 = W.赤ちゃん
c = [3.0]
v時定数 = 1000.0
class 換算(原):
    """つながり u（食べ物の増え）を、Q の物差しで学んだ一食の値打ち v食 で換算して足す。
    v食 ＝ 食べた次の手の TD 誤差の平均 − 食べなかった次の手の TD 誤差の平均（ゆっくりした平均）"""
    def __init__(s, 種, i, 頭):
        super().__init__(種, i, 頭); s.v食 = s.v有 = s.v無 = 0.0; s.前食 = None
    def 選ぶ(s, φ):
        q = s.Q @ φ
        ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
        score = q + c[0] * max(s.v食, 0.0) * u * ê
        a = int(np.argmax(score))
        if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
        return a, q, ê
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        if s.前 is not None and s.前食 is not None:
            φp, ap, Rp = s.前; δ = Rp + W.割引 * q[a] - s.Q[ap] @ φp
            if s.前食: s.v有 += (δ - s.v有) / v時定数
            else: s.v無 += (δ - s.v無) / v時定数
            s.v食 = s.v有 - s.v無
        super().受ける(φ, a, q, e, 食べた, 我慢); s.前食 = 食べた
v記録 = []
def 一生(種, 頭, 換算する=False, 寿命=8000):
    W.赤ちゃん = 換算 if 換算する else 原
    try: return W.一生(種, '依存', 頭, 寿命=寿命, 離乳=寿命)
    finally: W.赤ちゃん = 原
def 数字(o):
    _, _, 差 = W.区間の数字(o); return 差[0], float(np.mean(差[14:16]))

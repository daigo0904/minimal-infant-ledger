"""S129 相手に効く欠乏：大事な相手（つながり u が正）からの評価の、速い平均と遅い平均の差 d＝「最近もらえていない分」を持ち、
選びで、その相手の評価の予測 ê が一番高い手にだけ kD·d·重さ を足す（重さ＝clip(u/目安,0,1)）。kD=0 なら元の換算型と同じ手。"""
import numpy as np
設定 = dict(kD=0.0, 速=50.0, 遅=1000.0, 目安=0.02)
def に(基, W, B):
    class K(基):
        def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.速 = s.遅 = 0.0; s.始め = True
        def 選ぶ(s, φ):
            if 設定['kD'] == 0.0: return super().選ぶ(φ)
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
            score = q + B.c * max(s.v食, 0.0) * u * ê
            重さ = float(np.clip(u / 設定['目安'], 0, 1)); d = max(s.遅 - s.速, 0.0)
            score[int(np.argmax(ê))] += 設定['kD'] * d * 重さ
            a = int(np.argmax(score))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
        def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
            x = max(s.つながり.予測(φ), 0.0) / 設定['目安']; x = min(x, 1.0) * e   # 大事な相手からの評価（そうでない相手は 0）
            if s.始め: s.速 = s.遅 = x; s.始め = False
            s.速 += (x - s.速) / 設定['速']; s.遅 += (x - s.遅) / 設定['遅']
            return super().受ける(φ, a, q, e, 食べた, 我慢)
    return K

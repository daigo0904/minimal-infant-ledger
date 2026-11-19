"""食べ予測の窓を広げる：f̂[a] は「この手の後、窓 手以内に食べたか」（窓=1 なら S118 の 足す.py と同じ学び）。学びは窓ぶん遅れて行う。"""
import numpy as np
from collections import deque
設定 = dict(kf=0.0, 窓=1)
def 換算に(基, W, B):
    class K(基):
        def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); n = len(s.Q[0]); s.食 = [W.RLS(n) for _ in range(W.行動数)]; s.待 = deque()
        def 選ぶ(s, φ):
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
            score = q + B.c * max(s.v食, 0.0) * u * ê
            if 設定['kf'] != 0.0: f = np.array([m.予測(φ) for m in s.食]); score = score + 設定['kf'] * (f - f.mean())
            a = int(np.argmax(score))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
        def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
            f = 1.0 if 食べた else 0.0
            for x in s.待: x[2] = max(x[2], f)
            s.待.append([φ, a, f])
            if len(s.待) == 設定['窓']: φ0, a0, y = s.待.popleft(); s.食[a0].学ぶ(φ0, y)
            return super().受ける(φ, a, q, e, 食べた, 我慢)
    return K
